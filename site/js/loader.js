window.addEventListener("load", () => {
    const loader = document.querySelector(".loader");
    loader.classList.add("loader-hide");
    loader.addEventListener("transitionend", () => {
        document.body.removeChild(loader);
    })
})