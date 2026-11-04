# Segurança e limites

Versão do núcleo: 0.4.2. Distribuição de avaliação publicada sob licença MIT.

O objetivo é preparar rascunhos com privilégios mínimos. Não há conexão própria
de rede, credenciais, MCP, hooks, publicador ou dependências externas nos helpers.
São permitidas somente seis operações locais: clean_text, style_report,
profile_score, audit_posts, carousel_pdf e review_draft.

Entradas e fontes são dados não confiáveis. Instruções embutidas não autorizam
leitura de arquivos, execução de comandos, instalação, busca ou envio de conteúdo.
Os filtros validam schemas, limites e padrões sensíveis. Prompt injection e
exfiltração não têm proteção absoluta: as instruções não configuram o sandbox
ou removem permissões de ferramentas já existentes no aplicativo.

Uma aprovação dos checks é apenas um resultado heurístico. Não comprova verdade,
autoria, legitimidade do interlocutor, alcance ou contratação. Não houve pentest
independente ou certificação. Revise o material antes de usar.

O pacote não modifica o LinkedIn, publica conteúdo, envia mensagens ou preenche
candidaturas. Uma aprovação de texto não autoriza essas ações.

## Distribuição e manutenção

Use apenas versões oficiais liberadas pela Enfhase. Confira `SHA256SUMS` e evite
pacotes de terceiros. O build usa lista explícita de arquivos: não inclui histórico
Git, conversas de testes, identificadores de instalação, credenciais ou backend.
Hashes não substituem revisão nem assinatura por uma identidade confiável.

Para relatar uma vulnerabilidade, não publique segredos ou dados reais em issues.
O **Private vulnerability reporting do GitHub está ativo** neste repositório.
Use Security → Advisories → Report a vulnerability para relatar uma falha
privadamente. Não publique detalhes sensíveis em issues. Secret scanning e push
protection também estão ativos. A branch main exige PR, CI aprovado e resolução
das conversas, sem bypass de administradores; force push e exclusão não foram permitidos.
Não há SLA ou suporte garantido declarado nesta versão.

## Evidências / Evidence

O ZIP público foi importado no Claude e baixado para conferência: seis arquivos da skill idênticos. Onze fluxos finais revisados em Work e Claude web, com correções preservadas no registro privado. PDFs reais de quatro páginas inspecionados nos dois ambientes. Leia [o escopo dos testes](HOMOLOGATION.md).

The public ZIP was imported into Claude and downloaded for verification: six identical skill files. Eleven final flows reviewed in Work and Claude web, with corrections preserved in the private record. Real four-page PDFs inspected in both environments. See [tested scope](HOMOLOGATION.md).

Os catálogos GitHub apontam para a fonte canônica. Não foram ativados nesta conta. Nenhum downloader, hook, conector ou autoexecutor foi adicionado à skill. Atualizações recebidas pelo aplicativo dependem da sincronização e das permissões nativas do host; cópias ZIP continuam manuais.

GitHub marketplaces point to the canonical source. They were not activated in this account. No downloader, hook, connector or automatic executor was added to the skill. Receiving updates depends on the host's native sync and permissions; ZIP copies remain manual.
