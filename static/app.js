async function postJSON(url, payload){
  const res = await fetch(url, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload)
  });
  if(!res.ok){ throw new Error("Request failed"); }
  return res.json();
}

const $ = (q)=>document.querySelector(q);
const $$ = (q)=>document.querySelectorAll(q);

$("#btn-generate").addEventListener("click", async ()=>{
  const language = $("#language").value;
  const prompt = $("#prompt").value.trim();
  $("#output").textContent = "Generating...";
  try{
    const data = await postJSON("/api/generate", {language, prompt});
    if(data.ok){
      $("#code").value = data.code;
      $("#output").textContent = "Generated ✅";
    }else{
      $("#output").textContent = "Error: " + data.error;
    }
  }catch(e){
    $("#output").textContent = "Error: " + e.message;
  }
});

$("#btn-explain").addEventListener("click", async ()=>{
  const language = $("#language").value;
  const code = $("#code").value;
  $("#output").textContent = "Explaining...";
  try{
    const data = await postJSON("/api/explain", {language, code});
    if(data.ok){
      $("#output").textContent = data.explanation;
    }else{
      $("#output").textContent = "Error";
    }
  }catch(e){
    $("#output").textContent = "Error: " + e.message;
  }
});

$("#btn-debug").addEventListener("click", async ()=>{
  const language = $("#language").value;
  const code = $("#code").value;
  $("#output").textContent = "Debugging...";
  try{
    const data = await postJSON("/api/debug", {language, code});
    if(data.ok){
      const issues = (data.issues||[]).map(i=>"• "+i).join("\n");
      $("#output").textContent = (issues||"No obvious issues found.") + "\n\nSuggestion: " + data.suggestion;
    }else{
      $("#output").textContent = "Error";
    }
  }catch(e){
    $("#output").textContent = "Error: " + e.message;
  }
});

$("#btn-copy").addEventListener("click", async ()=>{
  try{
    await navigator.clipboard.writeText($("#code").value);
    $("#output").textContent = "Copied to clipboard ✅";
  }catch(e){
    $("#output").textContent = "Copy failed: " + e.message;
  }
});

$("#btn-download").addEventListener("click", ()=>{
  const blob = new Blob([$("#code").value], {type:"text/plain"});
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "codepal_snippet.txt";
  a.click();
  URL.revokeObjectURL(url);
});
