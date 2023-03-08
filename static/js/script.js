/// variáveis globais para armazenar os itens do carrinho e o total
let cartItems = {};
let cartTotal = 0;

const celulares = [];

const elementosCelular = document.querySelectorAll(".card-body");

elementosCelular.forEach(elemento => {
    const nomeCelular = elemento.querySelector("h5").textContent;
    const precoCelular = elemento.querySelector("p:nth-of-type(2)").textContent.replace('R$ ', '');
    celulares.push([nomeCelular, precoCelular]);
});

console.log(celulares);

// função para atualizar a tabela do carrinho
function atualizarCarrinho() {
    const carrinho = document.querySelector('.cart-table tbody');
    carrinho.innerHTML = '';

    // loop pelos itens do carrinho
    for (const item in cartItems) {
        const row = document.createElement('tr');
        // nome do item
        const nameCol = document.createElement('td');
        nameCol.textContent = cartItems[item].nome;
        row.appendChild(nameCol);

        // preço do item
        const priceCol = document.createElement('td');
        priceCol.textContent = 'R$ ' + cartItems[item].preco.toFixed(2);
        row.appendChild(priceCol);

        // quantidade do item
        const quantityCol = document.createElement('td');
        quantityCol.textContent = cartItems[item].quantidade;
        row.appendChild(quantityCol);

        carrinho.appendChild(row);
        // atualiza o total
        const totalContainer = document.querySelector('.cart-total-container span');
        totalContainer.textContent = 'R$ ' + cartTotal.toFixed(2);
    }
}

// função para adicionar um item ao carrinho
function adicionarAoCarrinho(idBotao) {
    // extrair o nome do celular do id do botão
    const nomeCelular = idBotao.split('-')[1];

    // encontrar o celular na lista de celulares
    const celular = celulares.find(celular => celular[0] === nomeCelular);


    // verificar se o celular foi encontrado
    if (celular) {
        // atualiza o objeto do carrinho
        const itemId = celular[0];
        const itemPreco = parseFloat(celular[1]);
        if (cartItems[itemId]) {
            cartItems[itemId].quantidade++;
            cartItems[itemId].total = itemPreco * cartItems[itemId].quantidade;
        } else {
            cartItems[itemId] = {
                nome: celular[0],
                preco: itemPreco,
                quantidade: 1,
                total: itemPreco
            };
        }
        // atualiza o total do carrinho
        cartTotal += itemPreco;

        // atualiza a tabela do carrinho
        atualizarCarrinho();
    } else {
        console.log('Celular não encontrado: ' + nomeCelular);
    }
}
