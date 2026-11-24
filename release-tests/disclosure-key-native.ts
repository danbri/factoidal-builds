import {deepStrictEqual, strictEqual} from "node:assert";

const [library, arm] = Deno.args;
const native = Deno.dlopen(library, {
  web_document_call: {parameters:["buffer","buffer","u32","u32"],result:"pointer"},
  web_render_free: {parameters:["pointer"],result:"void"},
} as const);
const cstr = (s:string) => new TextEncoder().encode(s+"\0");
function call(html:string, fields:Record<string,unknown>) {
  const request = {op:"scriptSession",url:"https://fixture.test/",engine:"bubblepop",...fields};
  const ptr = native.symbols.web_document_call(cstr(html),cstr(JSON.stringify(request)),640,480);
  if (!ptr) throw Error("No native answer");
  try {
    const answer = JSON.parse(new Deno.UnsafePointerView(ptr).getCString());
    if (answer.error||answer.inputError||answer.errors?.length) throw Error(JSON.stringify(answer));
    return answer;
  } finally {
    native.symbols.web_render_free(ptr);
  }
}
const cases = [
  {mode:"plain",clicks:1,opened:true},
  {mode:"keydown",clicks:0,opened:false},
  {mode:"keypress",clicks:0,opened:false},
  {mode:"keyup",clicks:0,opened:false},
  {mode:"click",clicks:1,opened:false},
  {mode:"blur",clicks:0,opened:false},
  {mode:"other",clicks:0,opened:false},
  {mode:"repeat",clicks:1,opened:true},
];
for (const {mode,clicks,opened} of cases) {
  const html = `<!doctype html>
<details><summary>More</summary><p>Body</p></details><div tabindex=0 id=other>Other focus</div>
<script>
const d=document.querySelector("details"), s=document.querySelector("summary"), other=document.querySelector("#other");
const m=${JSON.stringify(mode)};
for (const type of ["keydown","keypress","keyup","click"]) s.addEventListener(type,e => {
  console.log(JSON.stringify([type,d.open,e.isTrusted,e.repeat]));
  if(type===m)e.preventDefault();
  if(type==="keydown"&&m==="blur")other.focus();
});
const element=m==="other"?other:s;
element.focus();
console.log(JSON.stringify(["focus",document.activeElement===element]));
</script>`;
  const start = call(html, {action:"start"});
  deepStrictEqual(start.logs.map(JSON.parse),[["focus",true]]);
  try {
    const session = start.session;
    const act = (type:string) => call("",{action:"actions",session,actions:[
      {type:"key",id:"keyboard",actions:[{type,value:" "}]},
    ]});
    const first = act("keyDown");
    if (mode!=="blur") strictEqual(first.changed,false,`${mode} before release`);
    const again = mode==="repeat"?act("keyDown"):undefined;
    if (again) strictEqual(again.changed,false,"repeat before release");
    const last = act("keyUp");
    const logs = [...first.logs,...(again?.logs??[]),...last.logs].map(line=>JSON.parse(line));
    const observed = logs.filter(([type]:unknown[])=>type==="click");
    const candidate = arm === "candidate";
    strictEqual(last.changed,candidate&&opened,mode);
    strictEqual(observed.length,candidate?clicks:0,mode);
    if (candidate&&clicks) {
      deepStrictEqual(logs.at(-1).slice(0,3),["click",false,true],mode);
      deepStrictEqual(logs.at(-2).slice(0,3),["keyup",false,true],mode);
    }
    if (candidate&&mode!=="blur") strictEqual(first.keyDefault,mode==="other",mode);
    if (!candidate&&mode==="plain") strictEqual(first.keyDefault,true,mode);
    console.log(JSON.stringify({mode,keyDefault:first.keyDefault,changed:last.changed,logs}));
  } finally {
    call("",{action:"close",session:start.session});
  }
}
