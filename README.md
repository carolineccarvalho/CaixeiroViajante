<h1 align="center" style="font-weight: bold;">Trabalho Prático 2 de Algoritmos 2</h1>
<p align="center">
 <a href="#tech">Tecnologias</a> • 
 <a href="#intro">Introdução</a> • 
 <a href="#métodos">Métodos e Implementações</a> •
 <a href="#instrucoes">Instruções de Uso</a> • 
 <a href="#testes">Testes e Análise</a> • 
 <a href="#colab">Responsáveis</a> •
</p>
<p align="center">
    <b></b>
</p>

<h2 id="tech"> Tecnologias</h2>

- Python3

<h2 id="intro">Introdução</h2>
    O algoritmo LZW é uma extensão do algoritmo LZ78, com a principal diferença de que o LZW é inicializado com todos os símbolos do alfabeto das cadeias de entrada. Essa modificação permite que o algoritmo seja mais eficiente no processamento de dados, ao eliminar a necessidade de codificar explicitamente os símbolos isolados durante a compressão.

<h2 id="métodos">Métodos e Implementações</h2>
    Este projeto foi desenvolvido em três etapas principais: (1) a implementação do dicionário, (2) a implementação do algoritmo LZW para compressão e descompressão de dados com tamanho fixo, e (3) a implementação do algoritmo LZW para dados de tamanho variável. Todas as funcionalidades implementadas, bem como as escolhas de projeto, serão detalhadas nas seções a seguir.
<h3>Dicionário</h3>
<h4>Estrutura Geral</h4>
    <p>
    O dicionário foi implementado utilizando uma árvore de prefixos compacta. Essa abordagem reduz o consumo de memória ao representar cadeias longas, graças à compactação dos nós, e minimiza operações redundantes. A busca por palavras é realizada percorrendo as arestas da árvore, permitindo um acesso eficiente aos dados armazenados.
    </p>
    <p>
    Foram utilizadas duas classes ao todo. A primeira <code>TrieNode</code>, é responsável por representar os nós da árvore. Cada nó armazena duas informações: os filhos, que indicam se existem possíveis continuações para a cadeia armazenada no nó atual e o código único associado, utilizado para referenciar e diferenciar cada padrão. E a segunda <code>Dicionario</code>, é responsável por gerenciar a árvore de prefixos compacta, além de conectar essa estrutura à funcionalidade de um dicionário ao permitir que seja possível buscar palavras, retornar seus códigos associados, inserir novos padrões e remover entradas existentes.
    </p>
<h4>Funções Principais:</h4>
  <ul>
    <li>Dicionario() e ~Dicionario()</li>
    <p> 
    O construtor <code>Dicionario()</code> é responsável por inicializar a estrutura de dados, criando a raiz da árvore e conectando-a a dois filhos, um com o valor "0" e outro com o valor "1". Essa implementação está relacionada ao algoritmo LZW, que é inicializado com todos os simbolos do alfabeto das cadeias de entrada. Na nossa implementação, apenas esses dois caracteres são adicionados, pois estamos adotando uma implementação que aceitará e retornará cadeias binárias. O destrutor <code>~Dicionario</code> garante a liberação de memória, percorrendo e removendo todos os nós da árvore, evitando vazamentos de memória.
    </p> 
    <li>void insert(const string& palavra, const string& codigo)</li>
    <p>
    A função <code>insert()</code> é responsável por inserir novos padrões no dicionário. Para manter a estrutura da Trie Compacta, a inserção é feita da seguinte forma: a partir da raiz, o algoritmo verifica se algum dos filhos começa com o mesmo caractere da palavra que queremos adicionar, o que certamente ocorrerá devido à inicialização mencionada anteriormente. Em seguida, o algoritmo verifica se é possível agrupar prefixos em comum com os nós já existentes. Para cada filho, é analisado quanto do prefixo da palavra é comum ao valor da aresta do nó. Se nenhum filho correspondente for encontrado, o nó atual é atualizado para incluir a nova palavra e o código, criando um novo nó. Caso um filho correspondente seja encontrado, duas situações podem ocorrer: se o tamanho do prefixo comum for igual ao tamanho da aresta, o índice da palavra é avançado e o processo continua; se o prefixo comum for menor que o tamanho da aresta, o nó atual é dividido para manter a estrutura compacta.
    </p>
    <li>bool countTrie(const std::string& chave)</li>
    <p>
    A função <code>countTrie</code> verifica, de forma recursiva, se a chave especificada está presente na Trie. Ela percorre os nós e verifica a chave associada, e retorna <code>true</code> caso a chave seja encontrada. Caso contrário, retorna <code>false</code>.
    </p>
    <li>string getPalavra(const string& chave);</li>
    <p>
    A função <code>getPalavra</code> percorre recursivamente os nós da Trie, verificando se a chave fornecida corresponde a uma chave armazenada. Se a chave for encontrada, a função retorna a palavra associada a ela. Caso contrário, retorna uma string vazia.
    </p>
    <li>bool clear(const string& chave);</li>
    <p>
    A função <code>clear()</code> remove todos os nós da estrutura do dicionário, similar ao comportamento do destrutor da classe, e recria uma nova raiz para a Trie. Essa funcionalidade é especialmente útil nas operações de compressão e descompressão de textos com mais de 4000 caracteres, onde é necessário reinicializar o dicionário para continuar o processamento.
    </p>
    </ul>
<h4>Exemplos de Uso</h4>
<ul>
<li>Inserção</li>
<pre><code= cpp>
int main(){
    Dicionario dic;
    dic.insert("0001110", "1");
    dic.insert("0100010", "2");
    dic.insert("1001010", "3");
    dic.insert("1001000", "4");
    dic.insert("0001100", "5");
    dic.printTrie();
    return 0;
}
</code></pre>
<img src = "imagens/inserirTrie.png" alt = "inserirTrie" title = "InserirTrie" width="300">
<li>Busca</li>
<pre><code>
int main(){
    Dicionario dic;
    dic.insert("0001110", "1");
    dic.insert("0100010", "2");
    dic.insert("1001010", "3");
    dic.insert("1001000", "4");
    dic.insert("0001100", "5");
    cout << dic.countCode("5") << endl;
    cout << dic.getPalavra("5") << endl;
    return 0;
}
</code></pre>
<img src = "imagens/busca.png" alt = "buscaTrie" title = "BuscaTrie" width="400">
<li>Remoção</li>
<pre><code>
int main(){
    Dicionario dic;
    dic.insert("0001110", "1");
    dic.insert("0100010", "2");
    dic.insert("1001010", "3");
    dic.insert("1001000", "4");
    dic.insert("0001100", "5");
    cout << dic.countCode("5") << endl;
    cout << dic.getPalavra("5") << endl;
    return 0;
}
</code></pre>
<img src = "imagens/remove.png" alt = "removeTrie" title = "Removerie" width="300">
</ul>
<h3>LZW de tamanho variável</h3>
<p>
 O algoritmo LZW variável é executado através de duas funções <code>compression()</code> e <code>decompression()</code>, que serão explicadas a seguir:
</p>

<p>
O código da função <code>compression()</code> foi projetado para receber uma string como parâmetro e atribuir códigos a cada sequência de caracteres, que são então armazenadas em um dicionário (ou estrutura de dados semelhante a uma trie). Um aspecto importante dessa função é o controle de um inteiro auxiliar que rastreia a quantidade de códigos adicionados ao dicionário. A função também recebe um parâmetro inteiro chamado <code>max</code>, que representa o limite máximo de bits que podem ser usados para representar códigos. Enquanto esse auxiliar for menor ou igual ao valor de <code>max</code>, a função continua a adicionar novas sequências ao dicionário de forma incremental. No entanto, quando o auxiliar atinge um valor maior que <code>max</code>, a função deve redefinir esse auxiliar para 9 e esvaziar o dicionário para reiniciar a inserção de novas sequências.
</p>

<p>
A função <code>decompression()</code> descompacta uma sequência de códigos (<code>vector<int> codein</code>) que recebe como parâmetro. Inicialmente, ela constrói um dicionário com os caracteres ASCII e, conforme a descompressão avança, expande esse dicionário com novas sequências. O processo começa atribuindo o primeiro código à saída e iterando pelos demais códigos, verificando se a sequência existe no dicionário. Se não existir, trata-se de um caso especial que utiliza a própria sequência anterior para formar a nova entrada. O tamanho em bits (<code>bit</code>) aumenta conforme o dicionário cresce, mas, ao ultrapassar um limite máximo definido (<code>max</code>), o dicionário é reiniciado. Por fim, a função retorna a string descompactada como resultado final.
</p>
 
<h3>LZW de tamanho fixo</h3>
<p>
 O algoritmo LZW de tamanho fixo é executado através de duas funções <code>compressionFixed()</code> e <code>decompressionFixed()</code>, que serão explicadas a seguir:
</p>
<p>
A função <code>compressionFixed()</code> realiza a compressão de uma string <code>text</code>. Inicialmente, ela cria um dicionário com todas as representações dos caracteres ASCII, codificados com um tamanho de bits definido pelo usuário ou 12, por padrão. A compressão começa com a conversão do primeiro caractere em bits e analisa cada caractere subsequente para formar sequências. Se a sequência atual concatenada com o próximo símbolo existir no dicionário, a função continua . Caso contrário, a função armazena a sequência encontrada, insere a nova combinação no dicionário e, se o limite de bits for ultrapassado, reinicializa a dicionário e redefine o contador para manter o tamanho sob controle. A compressão é completada com a adição da última sequência ao vetor de saída, retornando assim um vetor de pares, onde cada par contém uma palavra compactada e o tamanho de sua representação.
</p>

<p>
A função <code>decompressionFixed()</code> realiza a descompressão de uma sequência de códigos. Ela começa obtendo o primeiro código, convertendo-o para sua representação e iniciando a saída com essa palavra. Para cada código subsequente, verifica se ele está no dicionário e, se não estiver, concatena a sequência anterior com seu primeiro caractere. Caso contrário, a entrada correspondente é recuperada do dicionário e adicionada à saída. Novas sequências são inseridas no dicionário até que o número de bits atinja o limite máximo, onde a trie é reinicializada. A função retorna a string descompactada após processar todos os códigos de entrada.
</p>

<h3>Funções intermediárias relevantes</h3>
<p>
 A função <code>openFile()</code> recebe o nome do arquivo, realiza a abertura de dele através do <code>ifstream</code> e retorna uma string com o conteúdo do arquivo.
</p>
<p>
 A função <code>write()</code> recebe o nome do arquivo original e escreve um um arquivo com a extensão .lzw. A string binária é convertida para binário com bitset e esse conteúdo é salvo no arquivo. Sua criação foi necessaria, pois, anteriormente, o valor que estava sendo salvo era uma string de 0 ou 1, que aumentava o tamanho do arquivo e não comprimia.
</p>
<p>
 A função <code>binary</code> pega o arquivo binário e transforma para uma string de zero e um, considerando os códigos binários em ASCII. Para essa execução, ele percorre cada caractere do texto e transforma esse caractere em uma string binária e concatena o resultado em uma variavel.
</p>
<p>
 A função <code>byteTobits()</code> transforma um caractere para sua string binária através do bitset.
</p>
<p>
 A função <code>savesize()</code> salva o tamanho em bit para cada código em um arquivo, em uma pasta "cache".
</p>
<p>
  A função <code>loadsize()</code> recupera o tamanho em bit para cada código localizada no arquivo.
</p>
<p>
  A função <code>save()</code> salva a string em um arquivo com a mesma extensão original.
</p>
<p>
  A função <code>apart()</code> divide a string binária de acordo com o tamanho de bit armazenado na pasta cache. Ela retorna um vetor de inteiro relacionado a cada string.
</p>
<p>
  As funções <code>compressionOPT()</code>, <code>decompressionOPT()</code>, <code>compressionFixedOPT()</code>, <code>decompressionFixedOPT()</code> são funções que executam o passo completo para a compressão ou descompressão. Sua criação foi necessária para facilitar a chamada no main.
</p>

<h2 id="instrucoes"> Instruções de Uso</h2>
 <p>
   1) Para compilar, é necessário escrever <code>make</code> na pasta raiz do projeto. Para executar, deve-se escrever <code>./main</code>.
  
   OBS: Por escolhas de projeto, na descompressão, o nome do arquivo a ser inserido é o mesmo do arquivo original, isto é, sem o ".lzw".
        Outro ponto se considerar é que tanto na compressão e descompressão, o arquivo deve estar na pasta raiz do projeto. 
 </p>
 <p>
 1) Para ter acesso aos gráficos e tabelas, é necessário que os seguintes passos sejam seguidos:
   <ol>
      <li>Acesse o seguinte link e siga o protocolo de instalação do Quarto: <a href="https://quarto.org/docs/get-started/">Quarto</a></li>
      <li> Certifique-se de que possui o ambiente configurado corretamente (RStudio, Visual Studio Code ou terminal).</li>
      <li> Abra o arquivo 'analiseDados.qmd' no ambiente de sua preferência. </li>
      <li> Para renderizar o relatório, execute o comando abaixo no terminal: quarto render analiseDados.qmd </li>
        (Certifique-se de estar no mesmo diretório do arquivo).
      <li> Após a execução, o relatório estará disponível no formato HTML, PDF ou outro, dependendo de como foi configurado.</li>
   </ol>
 </p>


<h2 id="testes"> Testes</h2>
<h3> Teste 1 - Livro Campo Geral</h3>
<img src="imagens/campo_geral.png" />
<h4>Compressão LZW Fixo</h4>
<p>
Ao rodar o comando "ls -l" no terminal é possível observar o tamanho do arquivo antes e depois da compressão, e portanto, concluir que ela de fato aconteceu.
</p>
<img src="imagens/terminaltcf.png"/>
<p>
A partir dessa compressão os seguintes dados foram gerados:
</p>
<img src="imagens/tabelatcf.png"/>
<p>
O seguinte gráfico facilita a visualização da compressão:
</p>
<img src="imagens/g1tcf.png"/>
<h4>Descompressão LZW Fixo</h4>
<p>
Ao rodar o comando "ls -l" no terminal é possível observar o tamanho do arquivo antes e depois da descompressão, note que o arquivo volta a ter o mesmo tamanho do arquivo original, indicando, assim, a descompressão.
</p>
<img src="imagens/terminaltdf.jpeg"/>
<p>
A partir dessa descompressão os seguintes dados foram gerados:
</p>
<img src="imagens/tabelatdf.jpeg"/>
<p>
O seguinte gráfico facilita a visualização da descompressão:
</p>
<img src="imagens/g1tdf.png"/>
<h4>Compressão LZW Variável</h4>
<p>
Ao rodar o comando "ls -l" no terminal é possível observar o tamanho do arquivo antes e depois da compressão, e portanto, concluir que ela de fato aconteceu.
</p>
<img src="imagens/terminaltcv.png"/>
<p>
A partir dessa compressão os seguintes dados foram gerados:
</p>
<img src="imagens/tabelatcv.jpeg"/>
<p>
O seguinte gráfico facilita a visualização da compressão:
</p>
<img src="imagens/g1tcv.png"/>
<h4>Descompressão LZW Variável</h4>
<p>
Ao rodar o comando "ls -l" no terminal é possível observar o tamanho do arquivo antes e depois da descompressão, note que o arquivo volta a ter o mesmo tamanho do arquivo original, indicando, assim, a descompressão.
</p>
<img src="imagens/terminaltdv.png"/>
<p>
A partir dessa descompressão os seguintes dados foram gerados:
</p>
<img src="imagens/tabelatdv.png"/>
<p>
O seguinte gráfico facilita a visualização da descompressão:
</p>
<img src="imagens/g1tdv.png"/>
<h3> Teste 2 - Imagem no formato .bmp</h3>
<p>
Os testes foram realizados com a seguinte imagem:
</p>
<img src="convert_to_image.bmp"/>
<h4>Compressão LZW Fixo</h4>
<p>
Ao rodar o comando "ls -l" no terminal é possível observar o tamanho do arquivo antes e depois da compressão, e portanto, concluir que ela de fato aconteceu.
</p>
<img src="imagens/terminalicf.png"/>
<p>
A partir dessa compressão os seguintes dados foram gerados:
</p>
<img src="imagens/tabelaicf.png"/>
<p>
O seguinte gráfico facilita a visualização da compressão:
</p>
<img src="imagens/g1icf.png"/>
<h4>Descompressão LZW Fixo</h4>
<p>
Ao rodar o comando "ls -l" no terminal é possível observar o tamanho do arquivo antes e depois da descompressão, note que o arquivo volta a ter o mesmo tamanho do arquivo original, indicando, assim, a descompressão.
</p>
<img src="imagens/terminalidf.jpeg"/>
<p>
A partir dessa descompressão os seguintes dados foram gerados:
</p>
<img src="imagens/tabelaidf.jpeg"/>
<p>
O seguinte gráfico facilita a visualização da descompressão:
</p>
<img src="imagens/g1idf.png"/>
<h4>Compressão LZW Variável</h4>
<p>
Ao rodar o comando "ls -l" no terminal é possível observar o tamanho do arquivo antes e depois da compressão, e portanto, concluir que ela de fato aconteceu.
</p>
<img src="imagens/terminalicv.png"/>
<p>
A partir dessa compressão os seguintes dados foram gerados:
</p>
<img src="imagens/tabelaicv.jpeg"/>
<p>
O seguinte gráfico facilita a visualização da compressão:
</p>
<img src="imagens/g1icv.png"/>
<h4>Descompressão LZW Variável</h4>
<p>
Ao rodar o comando "ls -l" no terminal é possível observar o tamanho do arquivo antes e depois da descompressão, note que o arquivo volta a ter o mesmo tamanho do arquivo original, indicando, assim, a descompressão.
</p>
<img src="imagens/terminalidv.png"/>
<p>
A partir dessa descompressão os seguintes dados foram gerados:
</p>
<img src="imagens/tabelaidv.jpeg"/>
<p>
O seguinte gráfico facilita a visualização da descompressão:
</p>
<img src="imagens/g1idv.png"/>
<h3> Teste 3 - imagem bmp</h3>
<img src="ponte.bmp" />
<h4>Compressão LZW Fixo</h4>
<p>
Ao rodar o comando "ls -l" no terminal é possível observar o tamanho do arquivo antes e depois da compressão, e portanto, concluir que ela de fato aconteceu.
</p>
<img src="imagens/terminalpcf.png"/>
<p>
A partir dessa compressão os seguintes dados foram gerados:
</p>
<img src="imagens/tabelapcf.jpg"/>
<p>
O seguinte gráfico facilita a visualização da compressão:
</p>
<img src="imagens/g1pcf.png"/>
<h4>Descompressão LZW Fixo</h4>
<p>
Ao rodar o comando "ls -l" no terminal é possível observar o tamanho do arquivo antes e depois da descompressão, note que o arquivo volta a ter o mesmo tamanho do arquivo original, indicando, assim, a descompressão.
</p>
<img src="imagens/terminalpdf.jpeg"/>
<p>
A partir dessa descompressão os seguintes dados foram gerados:
</p>
<img src="imagens/tabelapdf.jpeg"/>
<p>
O seguinte gráfico facilita a visualização da descompressão:
</p>
<img src="imagens/g1pdf.png"/>
<h4>Compressão LZW Variável</h4>
<p>
Ao rodar o comando "ls -l" no terminal é possível observar o tamanho do arquivo antes e depois da compressão, e portanto, concluir que ela de fato aconteceu.
</p>
<img src="imagens/terminalpcv.png"/>
<p>
A partir dessa compressão os seguintes dados foram gerados:
</p>
<img src="imagens/tabelapcv.jpeg"/>
<p>
O seguinte gráfico facilita a visualização da compressão:
</p>
<img src="imagens/g1pcv.png"/>
<h4>Descompressão LZW Variável</h4>
<p>
Ao rodar o comando "ls -l" no terminal é possível observar o tamanho do arquivo antes e depois da descompressão, note que o arquivo volta a ter o mesmo tamanho do arquivo original, indicando, assim, a descompressão.
</p>
<img src="imagens/terminalpdv.jpeg"/>
<p>
A partir dessa descompressão os seguintes dados foram gerados:
</p>
<img src="imagens/tabelapdv.jpeg"/>
<p>
O seguinte gráfico facilita a visualização da descompressão:
</p>
<img src="imagens/g1pdv.png"/>
<h2 id="colab"> Responsáveis</h2>
<table>
  <tr>
    <td align="center">
      <a href="#">
        <img src="https://avatars.githubusercontent.com/u/119982741?v=4" width="100px;" alt="Déborah picture"/><br>
        <sub>
          <b>Déborah Yamamoto</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#">
        <img src="https://avatars.githubusercontent.com/u/103433489?v=4" width="100px;" alt="Carol picture"/><br>
        <sub>
          <b>Caroline Carvalho</b>
        </sub>
      </a>
    </td>
  </tr>
</table>