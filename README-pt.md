# PyControl
Idiomas do README: [PT](README-pt.md) | [EN](README.md)

## Descrição
Script simples em python para controlar o mouse e teclado de outro computador, remotamente através da rede

## Pré-requisitos
1. [Python 3.x](https://www.python.org/downloads/).
2. [Instalador de pacotes para Python (pip)](https://pypi.org/project/pip/), para instalar o pynput.
3. [biblioteca pynput](https://pypi.org/project/pynput/), para 'escutar' e controlar o input do teclado e mouse.

## Atenção
Não é recomendado rodar este sript numa rede insegura.
Uma pessoa mal-intencionada poderia facilmente executar comandos arbitrários no computador servidor.

## Usando a ferramenta

### Iniciando o servidor
No computador que pretende controlar, execute o servidor.
Por padrão ele escutará na porta TCP 1234.
Para mantêr o código mais simples, não adicionei a opção de alterar a porta.
Caso queira alterar a porta, edite o valor da variável port (linha 12).

Para iniciar o servidor, execute:
```
./pycontrol.py
```

### Controlando o computador alvo
Para controlar o computador em questão, pegue o endereço IP do computador 
que está rodando o servidor e execute:

```
./pycontrol.py <ENDEREÇO>
```

### Tecla de escape
A tecla de escape desativa e ativa o controle do outro computador.
Por padrão a tecla é o Ctrl direito, mas você pode alterar isto adcionando
um terceiro argumento na linha 22, por exemplo:

```
client = Client(addr, port, Key.tab)
```
Isto irá alterar a tecla de escape para a tecla tab.

## Dica final
Você pode também controlar um computador fora da sua LAN, configurando um
redirecionamento de portas no seu roteador ou usando um serviço como [ngrok](https://ngrok.com/).

## Autores
* **Igor Costa Melo**
