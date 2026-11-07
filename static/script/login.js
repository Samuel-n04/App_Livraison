const mail = document.getElementById("mail");
const password = document.getElementById("password");

const formulaire = document.getElementById("formulaire");
let confirm = document.getElementById("confirm");

console.log("test");

async function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

// 58a9c6e
// d1JR33nh

formulaire.addEventListener("submit", async function (e) {
    e.preventDefault();

    if (mail == "" || password == "") {
        window.alert("Veuillez remplir tous les champs afin de vous authentifier");
        console.log("aa");
        return;
    }

    // window.location.replace("/register");

    try {
        const req = await fetch("/login", {
            method: "POST",
            body: new FormData(formulaire)
        });


        let resp = await req.json();

        if (resp.code == "ok") {
            console.log("yes")
            confirm.textContent = " Bienvenue dans votre session " + resp.nom + " " + resp.prenom;
            await sleep(2000);
            window.location.replace(resp.url);
        }

        else {
            console.log("no")
            confirm.textContent = resp.code + ":" + resp.message;
        }

    } catch (e) {
        window.alert("Erreur lors de la recherche");
    };




});


