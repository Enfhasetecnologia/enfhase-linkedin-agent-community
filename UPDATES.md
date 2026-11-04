# Atualizações / Updates

## Português

**ZIP manual:** baixe a nova versão e substitua a instalação. Ele não se atualiza sozinho.

**Sincronização automática:** o repositório inclui os catálogos necessários. Uma melhoria aprovada na `main` vira a fonte da próxima sincronização do aplicativo, sem servidor próprio ou chave de API.

- ChatGPT: disponível por importação de marketplace em workspace administrado. O administrador importa este repositório e mantém a sincronização diária. O menu da conta pessoal testada não ofereceu importação de marketplace; isso não foi ativado.
- Claude Code: adicione o marketplace e ative **Enable auto-update**. A próxima sessão carrega a atualização. Isso não comprova atualização automática no Claude Chat ou iPhone.
- Claude Chat: skills compartilhadas em Team/Enterprise acompanham a versão do proprietário; uma cópia por ZIP não acompanha o GitHub.

Não contrate plano nem mude permissões para seguir este guia. Sem o recurso nativo na sua conta, use o ZIP manual. Não há atualização remota pelo helper.

## English

**Manual ZIP:** download the new version and replace your installation. It does not update itself.

**Automatic sync:** this repository includes marketplace files. An improvement merged into `main` becomes the source for the app's next sync, with no custom server or API key.

- ChatGPT: an administrator can import this repository into a managed workspace and keep daily sync on. The tested personal account offered no marketplace import; this is not enabled.
- Claude Code: add the marketplace and select **Enable auto-update**. The next session loads the update. This does not validate automatic updates in Claude Chat or on iPhone.
- Claude Chat: skills shared on Team/Enterprise follow the owner's version; a ZIP copy does not follow GitHub.

Do not buy a plan or change permissions for this guide. If your account lacks native sync, use the manual ZIP. The helper never downloads or runs updates.

## Automação pessoal / Personal automation

Uma automação particular do mantenedor pode promover melhorias editoriais após merge e validação. Ela não atualiza cópias de outros usuários. Mudanças de código, segurança ou permissões precisam de revisão. Nenhuma contratação ou pagamento é autorizado; os limites da conta continuam valendo.

A maintainer's private automation can promote editorial improvements after merge and validation. It does not update other users' copies. Code, security or permission changes require review. No purchase or payment is authorized; account limits still apply.

## Para quem mantém / For maintainers

Altere a fonte em `native/enfhase-linkedin-agent`, atualize a versão em `plugin/plugin.json` e no builder, gere os pacotes e abra um PR. O CI testa o núcleo e reconstrói a distribuição automaticamente. Só a `main` revisada é fonte do catálogo. Não há promoção de branches de terceiros.

Edit `native/enfhase-linkedin-agent`, update the version in `plugin/plugin.json` and the builder, build the packages and open a PR. CI tests the core and rebuilds the distribution automatically. Only reviewed `main` is the catalog source. Third-party branches are not promoted.

## Fontes / Sources

- [OpenAI: GitHub marketplace sync](https://learn.chatgpt.com/docs/enterprise/plugin-management)
- [Anthropic: plugin updates](https://code.claude.com/docs/en/discover-plugins)
- [Anthropic: shared skills](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
