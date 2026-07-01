## ADDED Requirements

### Requirement: Rota de Sobre
O sistema SHALL registrar a rota `/sobre` mapeada para o componente `views/SobreView.vue`, acessível via link no rodapé, exibindo conteúdo institucional estático sobre o LegisKids.

#### Scenario: Acesso à página Sobre
- **WHEN** o usuário clica no link "Sobre" do rodapé
- **THEN** a URL muda para `/sobre` e o componente `SobreView` é renderizado, sem reload da página
