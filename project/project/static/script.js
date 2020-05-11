const paragrafo = document.querySelector('#paragrafo')




function writter (element) {
    const textArray = element.innerHTML.split('')
    element.innerHTML = ''
    textArray.forEach((letra, i) => {
        setTimeout(()=> {element.innerHTML += letra}, 90 *i)
    })
}

writter(paragrafo)

