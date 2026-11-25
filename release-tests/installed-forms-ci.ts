import {handle} from "./source/labs/demos/foafnaut/daily_use_server.ts";

const app = Deno.args[0];
const dir = Deno.args[1];
const server = Deno.serve({hostname:"127.0.0.1",port:0,onListen(){}},handle);
const cases = [
  {name:"plain-enter",path:"search.html",steps:["hold","tap:480,120","hold","type:hello",[5,36,0],"title=Results: hello"],expected:"hello"},
  {name:"scripted-click",path:"search-scripted.html",steps:["hold","tap:480,120","hold","type:two words","tap:1040,120","title=Results: two words"],expected:"two words"},
  {name:"empty-field",path:"search.html",steps:["hold","tap:480,120","hold","title=Search"]},
  {name:"typed-field",path:"search.html",steps:["hold","tap:480,120","hold","type:visible text","hold","title=Search"]},
];
const results = [];
try {
  for (const test of cases) {
    const file = dir + "/" + test.name + ".json";
    await Deno.writeTextFile(file, JSON.stringify(test.steps));
    const start = "http://127.0.0.1:" + server.addr.port + "/" + test.path;
    const child = new Deno.Command("timeout", {
      args:["70",app,"--offscreen","--no-state","--follow-links","--cookie-file",dir+"/cookies.txt",
        "--downloads",dir,"--url",start,"--steps",file,
        "--shot",dir+"/"+test.name+".png","--shot-at-end"],
      cwd:app.slice(0,app.lastIndexOf("/")), stdout:"piped",stderr:"piped",
    });
    const result = await child.output();
    const decode = new TextDecoder();
    const log = decode.decode(result.stdout) + decode.decode(result.stderr);
    await Deno.writeTextFile(dir+"/"+test.name+".log",log);
    const events = log.split("\n").filter(line=>line.startsWith("{")).flatMap(line=>{
      try { return [JSON.parse(line)]; } catch { return []; }
    });
    const submitted = events.some(event => event.type === "native-html-form-navigate" &&
      new URL(event.url).searchParams.get("q") === test.expected);
    const loaded = events.some(event => event.type === "native-html-loaded" &&
      new URL(event.url).pathname === "/results" && new URL(event.url).searchParams.get("q") === test.expected);
    const pass = result.code === 0 && (test.expected === undefined || submitted && loaded);
    const row = {test:test.name,pass,exit:result.code,submitted,loaded};
    results.push(row);
    console.log(JSON.stringify(row));
  }
} finally {
  await server.shutdown();
}
await Deno.writeTextFile(dir+"/results.json",JSON.stringify(results,null,2));
if (results.some(result=>!result.pass)) Deno.exit(1);
