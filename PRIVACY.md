# Privacidade do pacote nativo

Este documento descreve o código distribuído, sem substituir os termos do aplicativo de IA.

O pacote nativo não inclui telemetria, analytics, servidor Enfhase, conexão
LinkedIn ou chamadas próprias de rede. Ele não envia a conversa a outro provedor.
Se você escolher ChatGPT, conversa com a OpenAI; se escolher Claude, com a Anthropic.

O provedor recebe o texto enviado antes dos filtros locais. Histórico, treinamento,
retenção, exclusão, localização e permissões seguem a conta, as configurações e
os termos desse provedor. O pacote não controla esses aspectos.

Os helpers produzem resultados e recibos locais. O gerador de carrossel cria um
PDF em diretório temporário; o aplicativo controla sua retenção e disponibilização.
A distribuição nativa não inclui o backend privado nem sua auditoria SQLite.

Não envie senhas, tokens, cookies, documentos pessoais, dados bancários ou
informações confidenciais. Anonimize mensagens de terceiros e use apenas textos
próprios ou autorizados. Um bloqueio posterior não apaga dados já recebidos pelo provedor.

Não coloque conteúdo sensível em issues, comentários, screenshots ou relatórios
públicos. O canal escolhido para vulnerabilidades é o reporte privado do GitHub no futuro
repositório de distribuição, ainda pendente de ativação e verificação. Não use
issues públicas para dados pessoais. A descrição deve ser validada antes do lançamento.
