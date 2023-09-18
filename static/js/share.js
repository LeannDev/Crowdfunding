const content = document.getElementById('content');
const btnCapture = document.getElementById('btnCapture');
const aspectRatio = document.getElementById("ratio");

btnCapture.addEventListener('click', () => {

    content.style.borderRadius = "0";

    html2canvas(content).then(canvas => {
        const link = document.createElement('a');
        link.download = 'captura.png';
        link.href = canvas.toDataURL();
        link.click();
    });

    content.style.borderRadius = "1rem";
});

aspectRatio.addEventListener("change", () => {
    const ratioSelect = aspectRatio.value;
    content.style.aspectRatio = ratioSelect;
  });