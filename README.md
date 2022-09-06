# brasileirao
 Engajamento nos perfis do twitter dos clubes da Série A do Brasileirão 2022

Foi utilizada a API do Twitter para a captação dos dados, através da biblioteca Tweepy 4.10.1, do Python.

Foi utilizado o SQLite3 para armazenar e manipular os dados obtidos.

É realizada a leitura do arquivo tokens.txt, onde:
- a primeira linha corresponde a sua consumer_key
- a segunda linha corresponde a sua consumer_secret
- a terceira linha corresponde a sua access_token
- a quarta linha corresponde a sua access_token_secret
todas essas keys podem ser obtidas através de solicitação do https://developer.twitter.com/

Além disso, é lido o arquivo clubs.txt, onde cada linha corresponde ao exato @ do clube no twitter, é possível retirar ou adicionar outros clubes.

Por fim, é possível obter todos os tweets de todos os meses, alterando a constante MONTH, na função 'main', em main.py.