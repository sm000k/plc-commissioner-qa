"""Update v11 header and QA_LOG after adding encoder questions."""

# Update v11 header
content = open('docs/qa_draft_v11.md', encoding='utf-8').read()
content = content.replace('> **134 pytań / 19 sekcji.**', '> **137 pytań / 19 sekcji.**', 1)
content = content.replace('Pytania: 134', 'Pytania: 137', 1)
open('docs/qa_draft_v11.md', 'w', encoding='utf-8').write(content)
print('v11 header updated')

# Update QA_LOG
log = open('docs/QA_LOG.md', encoding='utf-8').read()
log = log.replace(
    '### Stan: 113 pytań, 19 sekcji — uniformalne enriched formatting przez WSZYSTKIE sekcje',
    '### Stan: 137 pytań, 19 sekcji — uniformalne enriched formatting + enkodery (3 nowe pytania)',
    1
)

old_end = ('- **Wynik:** jednolite formatowanie we WSZYSTKICH 19 sekcjach'
           ' (sekcje 11\u201319 dobrane do standardu sekcji 1\u201310)')
new_end = (old_end
           + '\n\n### Dodane pytania (2026-03-30 \u2014 enkodery):\n'
           + '- **Q1.15** "Czym jest enkoder \u2014 inkrementalny vs absolutny"'
           + ' \u2014 tabela por\xf3wnawcza, single-turn vs multi-turn, Safety encoder\n'
           + '- **Q16.12** "Parametry enkoder\xf3w \u2014 rozdzielczo\u015b\u0107,'
           + ' co mog\u0105 i czego nie mog\u0105" \u2014 PPR/bit, formu\u0142a pr\u0119dko\u015bci,'
           + ' ograniczenia Safety\n'
           + '- **Q16.13** "Interfejsy enkoder\xf3w i konfiguracja SINAMICS/TIA Portal"'
           + ' \u2014 TTL/HTL/Sin-Cos/SSI/EnDat/HIPERFACE; parametry p0400, p0404, p0418,'
           + ' konfiguracja Technology Object')
log = log.replace(old_end, new_end, 1)
open('docs/QA_LOG.md', 'w', encoding='utf-8').write(log)
print('QA_LOG updated')
