const [library,directory] = Deno.args;
const ffi = Deno.dlopen(library, {
  web_document_call: {parameters:["buffer","buffer","u32","u32"],result:"pointer"},
  web_document_call_bin: {parameters:["buffer","buffer","u32","u32","buffer"],result:"pointer"},
  web_render_free: {parameters:["pointer"],result:"void"},
} as const);
const input=JSON.parse(await Deno.readTextFile(directory+"/input.json"));
const html=await Deno.readTextFile(directory+"/page.html");
const encoder=new TextEncoder(),decoder=new TextDecoder();
const zero=(s:string)=>encoder.encode(s+"\0");
const width=1280, height=735;
const request=(options:Record<string,unknown>)=>zero(JSON.stringify({
  ...options,liberal:true,scripting:false,partialNote:false,checks:false,url:input.url,
}));
function inspect(source:string){
  const ptr=ffi.symbols.web_document_call(zero(source),request({op:"inspect"}),width,height);
  if(!ptr)throw Error("No response from inspect");
  try{
    const result=JSON.parse(new Deno.UnsafePointerView(ptr).getCString());
    if(result.error)throw Error(result.error);
    return result;
  }finally{ffi.symbols.web_render_free(ptr);}
}

const sheets=inspect(html).stylesheets as {nodeId:number;url:string}[];
const resources=sheets.flatMap(s=>Object.hasOwn(input.css,s.url) ? [{...s,source:input.css[s.url]}] : []);
const key="https://jvns.ca/stylesheets/noise.png";
if(!input.images[key]||resources.length<1)throw Error("Incomplete archived assets");

const gpu = Deno.args.includes("--gpu");
let device: GPUDevice | undefined;
let pipeline: GPURenderPipeline | undefined;
let pipelineShader: string | undefined;
if (gpu) {
  const adapter = await navigator.gpu.requestAdapter();
  if (!adapter) throw Error("No WebGPU adapter");
  device = await adapter.requestDevice();
}

async function measureGPU(wgsl: string, data: Uint8Array, tiles: Uint8Array, points: number[][]) {
  if (!device) throw Error("GPU device unavailable");
  device.pushErrorScope("validation");
  if (!pipeline) {
    const module = device.createShaderModule({code: wgsl});
    const diagnostics = (await module.getCompilationInfo()).messages.filter(entry=>entry.type === "error");
    if (diagnostics.length) throw Error(diagnostics.map(entry=>entry.message).join("\n"));
    pipeline = await device.createRenderPipelineAsync({
      layout:"auto",vertex:{module,entryPoint:"vertex"},
      fragment:{module,entryPoint:"fragment",targets:[{format:"rgba8unorm"}]},
    });
    pipelineShader = wgsl;
  } else if (wgsl !== pipelineShader) throw Error("The fixture changed shader source");

  const upload = (bytes: Uint8Array) => {
    const buffer = device!.createBuffer({size:bytes.byteLength,usage:GPUBufferUsage.STORAGE | GPUBufferUsage.COPY_DST});
    device!.queue.writeBuffer(buffer,0,Uint8Array.from(bytes));
    return buffer;
  };
  const params = upload(data), spatial = upload(tiles);
  const texture = device.createTexture({size:[width,height],format:"rgba8unorm",
    usage: GPUTextureUsage.RENDER_ATTACHMENT | GPUTextureUsage.COPY_SRC});
  const stride = Math.ceil(width*4/256)*256;
  const readback = device.createBuffer({size:stride*height,usage:GPUBufferUsage.COPY_DST | GPUBufferUsage.MAP_READ});
  try {
    const group = device.createBindGroup({layout:pipeline.getBindGroupLayout(0),entries:[
      {binding:0,resource:{buffer:params}}, {binding:1,resource:{buffer:spatial}},
    ]});
    const commands = device.createCommandEncoder();
    const pass = commands.beginRenderPass({colorAttachments:[
      {view:texture.createView(),clearValue:{r:1,g:1,b:1,a:1},loadOp:"clear",storeOp:"store"},
    ]});
    pass.setPipeline(pipeline);
    pass.setBindGroup(0,group);
    pass.draw(3);
    pass.end();
    commands.copyTextureToBuffer({texture},{buffer:readback,bytesPerRow:stride,rowsPerImage:height},[width,height,1]);
    device.queue.submit([commands.finish()]);
    const error = await device.popErrorScope();
    if (error) throw Error(error.message);
    await readback.mapAsync(GPUMapMode.READ);
    const pixels = new Uint8Array(readback.getMappedRange());
    return points.map(([x,y])=>[...pixels.subarray(y*stride+x*4,y*stride+x*4+3)]);
  } finally {
    readback.destroy();
    texture.destroy();
    spatial.destroy();
    params.destroy();
  }
}

async function measure(name:string,source:string,points:number[][],options:Record<string,unknown>={}){
  const size=new Uint32Array(1);
  const ptr=ffi.symbols.web_document_call_bin(zero(source),request({
    op:"render",cpu:true,diagnostics:true,...options,
  }),width,height,size);
  if(!ptr)throw Error("No render response");
  try{
    const data=Deno.UnsafePointerView.getArrayBuffer(ptr,size[0]);
    const header=new DataView(data);
    const length=header.getUint32(4,true),sections=header.getUint32(8,true);
    const body=12+4*sections;
    const meta=JSON.parse(decoder.decode(new Uint8Array(data,body,length)));
    if(meta.error || typeof meta.pixelsSection!=="number")throw Error(meta.error??"No CPU pixels");
    const section = (index: number) => {
      let seek=body+length;
      for(let i=0;i<index;i++)seek+=(header.getUint32(12+4*i,true)+3)&~3;
      return new Uint8Array(data,seek,header.getUint32(12+4*index,true));
    };
    const image=section(meta.pixelsSection);
    if(image.length!==width*height*4)throw Error("Wrong raster bounds");
    const colors=points.map(([x,y])=>[...image.subarray((y*width+x)*4,(y*width+x)*4+3)]);
    const gpuColors=meta.wgsl && gpu
      ? await measureGPU(meta.wgsl,section(meta.dataSection),section(meta.tilesSection),points)
      : undefined;
    if (gpu && !gpuColors) throw Error("Missing GPU readback");
    console.log(JSON.stringify({name,colors,gpuColors,diagnostics:meta.diagnostics??[]}));
  }finally{ffi.symbols.web_render_free(ptr);}
}

await measure("jvns",html,Array.from({length:119},(_,i)=>[25,100+i]),
  {resources,images:[{key,base64:input.images[key]}]});

const png="iVBORw0KGgoAAAANSUhEUgAAAAEAAAACCAIAAAAW4yFwAAAAEElEQVR4nGP4z8DAwMDwHwAIAAH/B2G9UwAAAABJRU5ErkJggg==";
for(const repeat of ["repeat","repeat-x","repeat-y","no-repeat"]){
  const css=`body{margin:0}div{width:400px;height:300px;background:white url(data:image/png;base64,${png}) 7px 5px /`+
    `1px 2px ${repeat}}`;
  await measure(repeat,`<!doctype html><style>${css}</style><div></div>`,
    [[7,5],[7,6],[7,123],[199,5],[199,123],[410,123]]);
}
const fractional=`body{margin:0}div{width:400px;height:300px;background:white url(data:image/png;base64,${png}) 2.25px 3.5px / 1.5px 2.25px repeat}`;
await measure("fractional",`<!doctype html><style>${fractional}</style><div></div>`,
  [[0,0],[1,2],[8,5],[7,123],[199,5],[199,123],[398,297],[410,123]]);
device?.destroy();
