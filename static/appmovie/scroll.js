export default function ScrollBar(){
    document.querySelectorAll(".row-container").forEach(container => {
    
    const leftBtn = container.querySelector(".left");
    const rightBtn = container.querySelector(".right");
    const slider = container.querySelector(".movie-row");

    leftBtn.addEventListener("click", () => {
        slider.scrollBy({
            left: -slider.offsetWidth,
            behavior: "smooth"
        });
    });

    rightBtn.addEventListener("click", () => {
        slider.scrollBy({
            left: slider.offsetWidth,
            behavior: "smooth"
        });
    });

});
}