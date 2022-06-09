# sgceScripts

Este projeto apresenta diferentes _scripts_ que funcionam como base e suporte para o projeto [UTF Certificados](https://github.com/pradoplucas/utfCerts). Os _scripts_ são responsáveis por buscar, organizar, criar, salvar e atualizar os dados necessários.

## Instalação

### Primeiramente, tenha instalado em sua máquina
- `Python`, juntamente com o `PIP`;
- `MongoDB`, juntamente com o `MongoDB Shell`;
- `git`.

### Após isso, instale as seguintes bibliotecas do Python através do pip
- `beautifulsoup4`: Screen-scraping library;
- `Levenshtein`: Computing string edit distances and similarities;
- `pymongo`: Python driver for MongoDB;
- `Unidecode`: ASCII transliterations of Unicode text.

### E por fim, clone o repositório do projeto
```bash
$ git clone https://github.com/pradoplucas/sgceScripts.git
```

## Como Usar

### Comandos

```
y       determina o ano (4 digítos)
```

### Obtendo os dados

```bash
$ python init.py y 'yyyy'
```

### Criando e salvando no Banco de Dados

```bash
$ python create.py
```

### Atualizando o Banco de Dados

```bash
$ python update.py y 'yyyy'
```

## Contribuindo

### Reportar _Bug_ & Solicitar _Feature_

Use o [_issue tracker_](https://github.com/pradoplucas/sgceScripts/issues) para reportar algum _bug_ ou solicitar uma nova _feature_.

### Desenvolvendo

Novos _Pull Requests_ são bem-vindos.

1. Dê _Fork_ no Projeto;
2. Crie sua _Branch_ (`git checkout -b feature/AmazingFeature`);
3. Faça _Commit_ em suas mudanças (`git commit -m 'Add some AmazingFeature'`);
4. Faça o _Push_ para a _Branch_ (`git push origin feature/AmazingFeature`);
5. Abra um _Pull Request_.

## Contato

### Lucas do Prado Pinto - lucaspinto@alunos.utfpr.edu.br

- [Página Pessoal](https://pradoplucas.github.io/)
- [GitHub](https://github.com/pradoplucas/)
- [Linkedin](https://www.linkedin.com/in/pradoplucas/)
- [Lattes](http://lattes.cnpq.br/7589155295539184)
- [Instagram](https://www.instagram.com/pradoplucas/)
- [Facebook](https://www.facebook.com/pradoplucas)
- [Twitter](https://twitter.com/pradoplucas)

Link do projeto: [https://github.com/pradoplucas/sgceScripts](https://github.com/pradoplucas/sgceScripts)
