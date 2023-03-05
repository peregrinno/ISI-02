
function adicionarAoCarrinho(btnId) {
    var celularNome = btnId.split('-')[1];
    atualizarCarrinho(celularNome);
}