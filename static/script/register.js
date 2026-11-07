const confirm = document.getElementById("confirm");
const form = document.getElementById("formulaire");

async function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}


form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const req = await fetch("/register", {
        method: "POST",
        body: new FormData(form)
    });
    const data = await req.json();

    if (data.code == "Created") {
        confirm.textContent = "Inscription Validée, Bienvenue " + data.nom + " " + data.prenom;
        sleep(2000);

        window.location.replace(data.url);


    } else {
        confirm.textContent = data.message || "Erreur";
    }
})

async function confirm_database() {

}