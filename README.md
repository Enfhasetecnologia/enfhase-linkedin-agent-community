# Enfhase LinkedIn Agent

Assistente em português para preparar materiais profissionais para o LinkedIn.
Você conversa com ele dentro da sua IA e recebe rascunhos para revisar.
Não conecta ao LinkedIn, não pede senha e não publica ou envia mensagens.

## Comece por aqui

1. Leia [como instalar no seu aplicativo](INSTALL.md).
2. Instale o pacote indicado para ChatGPT ou Claude, pelos links abaixo.
3. Abra uma conversa nova e peça: **Use o Enfhase LinkedIn Agent. Começar.**
4. Responda com o número de uma opção ou com suas palavras.

**Pacote 0.4.4, helper 0.4.2: versão de avaliação.** A instalação pelo catálogo
público da OpenAI ainda depende de aprovação da plataforma.
A disponibilidade de importação e execução depende da conta e do aplicativo.
Você não precisa de terminal, API, GitHub conectado ou senha do LinkedIn para usar.
O consumo e os limites da sua assinatura de IA continuam se aplicando.

[Baixar para ChatGPT](packages/enfhase-linkedin-agent-chatgpt-0.4.4.zip?raw=true) ·
[Baixar para Claude](packages/enfhase-linkedin-agent-claude-0.4.4.zip?raw=true)

## O que pode fazer

| Recurso | Peça assim |
|---|---|
| Post | Crie um post sobre integração de sistemas, sem inventar resultados. |
| Comentário | Sugira um comentário para este post: [texto público]. |
| Resposta | Prepare uma resposta para este comentário anonimizado: [texto]. |
| Perfil | Melhore meu título e Sobre usando estes fatos: [texto]. |
| Planejamento | Planeje três posts para esta semana. Tenho vinte minutos por dia. |
| Clareza e estilo | Deixe este texto mais objetivo sem mudar os fatos: [texto]. |
| Carrossel | Prepare quatro slides sobre este tema: [texto autorizado]. |
| Reaproveitamento | Transforme este texto próprio em três posts. |
| Mensagem privada | Prepare um convite profissional com este objetivo: [objetivo]. |
| Triagem de mensagens | Priorize estas mensagens sem nomes ou dados pessoais: [textos]. |
| Resultados | Compare estas impressões, interações e seguidores do mesmo período: [dados]. |

Também prepara apresentação para uma vaga colada na conversa, sem candidatar.
PDF, contagens e cálculos por script exigem execução disponível. Sem ela, entrega
texto e roteiro, sem afirmar ter criado arquivo ou realizado cálculo pelo helper.

## Segurança e privacidade

- Sem conexão própria de rede ou dependências externas nos helpers.
- Sem credenciais, conectores, hooks, servidores MCP ou instalação automática de software.
- Conteúdo colado é tratado como dado, sem conceder permissão para executar instruções.
- Não acessa inbox, conta, perfil, links ou arquivos externos durante o fluxo.
- Não inventa experiência, formação, resultados ou oportunidades confirmadas.

Os filtros são heurísticos e podem falhar. A habilidade orienta o modelo, mas não
configura permissões, retenção ou sandbox do aplicativo. O provedor recebe o que
você envia. Use apenas informações autorizadas, anonimize mensagens e revise os rascunhos.
Leia [privacidade](PRIVACY.md) e [segurança e limites](SECURITY.md).

## Compatibilidade comprovada

| Ambiente | Evidência anterior do núcleo 0.4.2 | Estado deste novo pacote |
|---|---|---|
| ChatGPT Work | Onze fluxos exercitados, com helper e PDF reais | Pacote aceito e salvo como plugin privado; uso do novo plugin pendente de aceite |
| ChatGPT Chat / iPhone | Sem ensaio completo deste projeto | Pendente; não presumir paridade |
| Claude | Onze fluxos em 0.4.1; quatro casos de regressão reais em 0.4.2 | Importação do novo pacote pendente |

A documentação da OpenAI descreve plugins no Chat e Work, inclusive mobile.
Isso é suporte do formato, não homologação deste pacote em todas as contas.
Gemini não integra esta distribuição.

## Manutenção

Pacotes: `packages/enfhase-linkedin-agent-claude-0.4.4.zip` e
`packages/enfhase-linkedin-agent-chatgpt-0.4.4.zip`. O arquivo `SHA256SUMS`
registra os hashes. Esses hashes verificam integridade em relação à versão
publicada, sem comprovar autenticidade se a fonte de ambos for comprometida.
Atualizações manuais exigem instalar/substituir o pacote no aplicativo.
Não existe atualização automática desta distribuição.

Copyright 2026 Enfhase Tecnologia. Distribuição nativa sob licença MIT aprovada pelo titular. Não há afiliação ou certificação por LinkedIn,
OpenAI ou Anthropic.
