// Funzione generica per detectare una specifica lettera dalla tastiera
function detectKeyPress(letter, callback) {
    document.addEventListener('keydown', (event) => {
        if (event.key.toLowerCase() === letter.toLowerCase()) {
            callback(letter);
        }
    });
}

// Funzione per gestire la pressione di una lettera
function handleKeyPress(letter) {
    console.log(`Lettera premuta: ${letter}`);
    // Aggiungi qui la logica personalizzata per ogni lettera
    const button = document.querySelector(`button[value = "${letter.toLowerCase()}"]`);
    if ( button ){
        button.click();
    }
}

// Funzione alternativa: detectare tutte le lettere dalla tastiera
function detectAllKeyPresses() {
    document.addEventListener('keydown', (event) => {
        if (/^[a-z]$/i.test(event.key)) {
            console.log(`Hai premuto la lettera: ${event.key}`);
            handleKeyPress(event.key);
        }
    });
}

// Funzione per detectare più lettere contemporaneamente
function detectMultipleKeys(letters, callback) {
    document.addEventListener('keydown', (event) => {
        if (letters.includes(event.key.toLowerCase())) {
            console.log(`Hai premuto la lettera: ${event.key}`);
            callback(event.key.toLowerCase());
        }
    });
}

// Inizializza i listener quando il DOM è carico
document.addEventListener('DOMContentLoaded', () => {
    // Opzione 1: Detectare singole lettere
    detectKeyPress('w', handleKeyPress);
    detectKeyPress('a', handleKeyPress);
    detectKeyPress('s', handleKeyPress);
    detectKeyPress('d', handleKeyPress);
    detectKeyPress(' ', handleKeyPress);

    // Opzione 2: Detectare tutte le lettere (decommentare se preferito)
    // detectAllKeyPresses();

    // Opzione 3: Detectare solo lettere specifiche con una sola funzione
    // detectMultipleKeys(['w', 'a', 's', 'd'], (letter) => {
    //     console.log(`Azione personalizzata per ${letter}`);
    // });
});
