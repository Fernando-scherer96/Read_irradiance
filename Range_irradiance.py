def categorizar_irradiancia(valor): 
    if valor > 875: 
        return 'Faixa F'
    elif 625 <= valor <= 875: 
        return 'Faixa E'
    elif 400 <= valor <= 625: 
        return 'Faxia D'
    elif 250 <= valor <= 400:
        return 'Faixa C'
    elif 150 <= valor <= 250:
        return 'Faixa B'
    else:
        return 'Faixa A'
    