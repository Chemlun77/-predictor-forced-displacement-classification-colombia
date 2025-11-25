ESTADO_DEPTO_MAPPING = {
    'Nari�o': 'Nariño',
    'Archip.De San Andres, Providencia y Santa Catalina': 'Archipielago de San Andrés, Providencia y Santa Catalina',
}

ETNIA_MAPPING = {
    'Indigena (Acreditado RA)': 'Indigena',
    'Negro(a) o Afrocolombiano(a)': 'Afrocolombiano(a)',
    'Negro (Acreditado RA)': 'Afrocolombiano(a)',
    'Afrocolombiano (Acreditado RA)': 'Afrocolombiano(a)',
    'Gitano(a) ROM': 'Gitano(a)',
    'Gitano (RROM) (Acreditado RA)': 'Gitano(a)',
    'Palenquero (Acreditado RA)': 'Palenquero'
}

CICLO_VITAL_MAPPING = {
    'entre 29 y 60': 'entre 29 y 59',
    'entre 61 y 100': 'entre 60 y 110'
}

HECHO_MAPPING = {
    'Desaparici�n forzada': 'Desaparición forzada',
    'DesapariciÃ³n forzada': 'Desaparición forzada',
    'Vinculaci�n de Ni�os Ni�as y Adolescentes a Actividades Relacionadas con grupos armados': 
        'Vinculación de Niños Niñas y Adolescentes a Actividades Relacionadas con grupos armados',
    'VinculaciÃ³n de NiÃ±os NiÃ±as y Adolescentes a Actividades Relacionadas con grupos armados':
        'Vinculación de Niños Niñas y Adolescentes a Actividades Relacionadas con grupos armados',
    'Minas Antipersonal, Munici�n sin Explotar y Artefacto Explosivo improvisado':
        'Minas Antipersonal, Munición sin Explotar y Artefacto Explosivo improvisado',
}

VALUES_TO_REMOVE = {
    'ESTADO_DEPTO': ['SIN DEFINIR'],
    'SEXO': ['No Informa'],
    'DISCAPACIDAD': ['Por Establecer'],
    'CICLO_VITAL': ['ND'],
    'HECHO': ['Sin informacion']
}
