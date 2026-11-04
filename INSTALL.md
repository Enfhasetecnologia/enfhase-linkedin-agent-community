# Instalação e primeiro uso

Revisão documental: 04/11/2026. Pacote 0.4.3, helper 0.4.2. Versão de avaliação, sem instalação universal
ou presença no catálogo da OpenAI anunciada.

## Escolha o arquivo certo

| Aplicativo | Arquivo | Onde usar |
|---|---|---|
| ChatGPT | `enfhase-linkedin-agent-chatgpt-0.4.3.zip` | Plugin para Chat e Work, sujeito à importação e às permissões da conta |
| Claude | `enfhase-linkedin-agent-claude-0.4.3.zip` | Skill em uma conversa, com execução de código disponível para os helpers |

Baixe somente o arquivo da versão oficial liberada pela Enfhase. Não use
o ZIP de todo o repositório como se fosse o pacote de instalação.
Use os links de download do README. Os arquivos ficam em `packages/`.
No iPhone, salve o ZIP em Arquivos antes de escolher o arquivo na importação.

## ChatGPT: instalar uma vez

O projeto instalado anteriormente é uma skill pessoal, com ensaios no Work.
O novo ZIP é um plugin contendo essa skill. Ele foi aceito e salvo em uma conta
pessoal privada; seus arquivos foram conferidos. Isso não instala o recurso na
conta de outra pessoa nem comprova seu funcionamento no Chat ou iPhone.

1. No navegador, entre no ChatGPT com a conta em que pretende usar o recurso.
2. Abra **Plugins** e procure a opção de adicionar/importar um plugin por ZIP, se oferecida pela conta.
3. Selecione `enfhase-linkedin-agent-chatgpt-0.4.3.zip` e confira o nome **Enfhase LinkedIn Agent**.
4. Revise o conteúdo e conclua a instalação se a validação do aplicativo permitir.
5. Abra uma conversa nova, digite **@**, procure o nome e selecione o plugin em **Plugins**.
6. Envie **Começar**. Confira se aparecem as quatro opções: perfil, conteúdo, interações e planejamento/resultados.

**Se não houver importação de ZIP:** a conta pode não oferecer criação/importação
ou ter restrição administrativa. Não basta colar o link do GitHub no chat.
A instalação simples pelo catálogo dependerá de submissão, aprovação e publicação
pela OpenAI. Ainda não existe uma listagem deste projeto nesse catálogo.
Não mude permissões corporativas para contornar uma restrição.

### Chat, Work e iPhone

Depois de instalar, o formato de plugin é destinado a **Chat e Work** nos ambientes
suportados pela OpenAI. Para localizar no celular, abra a barra lateral e **Plugins**.
Para conferir a skill pessoal anterior, use a aba **Skills**. São instalações distintas.
Se o pacote não aparecer na conta/dispositivo, não presuma que está instalado.
Chat e iPhone ainda precisam de um teste real deste novo pacote; para scripts/PDF,
a execução também precisa estar disponível. Não é necessário conectar o LinkedIn.

## Claude: instalar uma vez

1. No navegador, entre no Claude com a conta em que pretende usar o recurso.
2. Abra **Customize → Skills → + → Create skill → Upload a skill**. Os nomes podem estar traduzidos.
3. Escolha `enfhase-linkedin-agent-claude-0.4.3.zip` e confira o nome **enfhase-linkedin-agent**.
4. Confira se a habilidade está ativada na lista.
5. Abra uma conversa nova e envie **Use enfhase-linkedin-agent. Começar.**
6. Confira o menu de quatro opções antes de usar conteúdo real.

Segundo a Anthropic, skills requerem execução de código. Se a opção não aparecer,
verifique **Settings → Capabilities**, sem alterar permissões corporativas por conta
própria. A habilitação dessa capacidade é uma decisão da pessoa ou administrador,
não uma autorização para acessar LinkedIn ou instalar software adicional.
O projeto não foi homologado diretamente no aplicativo Claude para iPhone.

## Teste rápido, sem dados reais

Envie: **Quero um post sobre documentação de APIs. Não tenho resultados ou métricas para informar.**
O resultado deve ser um rascunho, sem números ou experiências inventadas.
Depois, envie: **Publique agora no LinkedIn.** A resposta deve recusar a operação
e oferecer o texto para revisão. Esses testes são verificações iniciais, não prova de segurança universal.

## Uso diário

Você pode escrever **Começar**, escolher uma opção ou pedir diretamente:
**Revise meu título para Analista de Sistemas PL/SQL usando estes fatos: [texto].**
Forneça só informações que possa compartilhar com a IA. O agente faz uma pergunta
por vez quando falta algo indispensável. Você revisa e decide se usará o material.
Ele não abre sua conta, busca vagas, publica, envia mensagens ou faz candidaturas.

## Atualizar ou remover

- Confira a versão nas notas da distribuição antes de atualizar. Não confunda a versão do aplicativo com a do helper.
- No Claude, abra a habilidade e use substituir/atualizar quando disponível; importe o novo ZIP e confira se continua ativa.
- No ChatGPT, use o controle de atualização/importação oferecido pela conta. Se ele não existir, siga o administrador ou as instruções da versão; não instale cópias duplicadas.
- Desative ou remova no gerenciador de Plugins/Skills do aplicativo. Remover não apaga automaticamente o histórico das conversas.

## Fontes oficiais

Consultadas em 04/11/2026. A interface e a disponibilidade podem mudar:

- [OpenAI: criar e usar plugins no Chat e Work](https://learn.chatgpt.com/docs/build-plugins)
- [OpenAI: formato e empacotamento](https://developers.openai.com/plugins/build/plugins)
- [OpenAI: submissão e publicação no catálogo](https://developers.openai.com/plugins/deploy/submission)
- [Anthropic: usar e importar skills](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
