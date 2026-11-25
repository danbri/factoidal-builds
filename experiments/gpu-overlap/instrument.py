from pathlib import Path
import sys
path = Path(sys.argv[1])
output = Path(sys.argv[2])
source = path.read_text()

def replace(source, old, new):
    assert source.count(old) == 1, old
    return source.replace(old,new)

source = replace(source, '  let document=await prepareHTML(lean,url,', '''  const startupPhase=(phase:string)=>console.log(JSON.stringify({type:"native-html-startup-overlap",phase,t:performance.now()}));
  const pickAdapter=async()=>{
    startupPhase("adapter-start");
    try { return await navigator.gpu?.requestAdapter(); }
    finally { startupPhase("adapter-end"); }
  };
  const openDevice=async(adapter:GPUAdapter)=>{
    startupPhase("device-start");
    try { return await adapter.requestDevice(); }
    finally { startupPhase("device-end"); }
  };
  startupPhase("document-start");
  const requestedDocument=prepareHTML(lean,url,''')
source = replace(source, '  }),width=windowSize?.[0]??1280,height=windowSize?.[1]??800;', '''  });
  STARTUP_OVERLAP
  let document=await requestedDocument,width=windowSize?.[0]??1280,height=windowSize?.[1]??800;
  startupPhase("document-end");''')
source = replace(source, '  const adapter=await navigator.gpu?.requestAdapter();', '  const adapter=await STARTUP_ADAPTER;')
source = replace(source, '    device=await adapter.requestDevice();native=early??', '    device=await STARTUP_DEVICE;native=early??')
baseline=source.replace('  STARTUP_OVERLAP\n','').replace('STARTUP_ADAPTER','pickAdapter()').replace('STARTUP_DEVICE','openDevice(adapter)')
candidate=source.replace('  STARTUP_OVERLAP', '''  // The first document is already in flight and does not need a surface or GPU.
  const pickedAdapter=check?undefined:pickAdapter();
  const openedDevice=pickedAdapter?.then(adapter=>adapter?openDevice(adapter):undefined);
  void openedDevice?.catch(()=>{});''').replace('STARTUP_ADAPTER','pickedAdapter').replace('device=await STARTUP_DEVICE;','device=await openedDevice;\n    if(!device)throw new Error("Native HTML: GPU device unavailable");\n    ')
output.mkdir(parents=True,exist_ok=True)
(output/'a.ts').write_text(baseline)
(output/'b.ts').write_text(candidate)
