# catalogo de escenarios tematicos y retos sintacticos accesibles con mapeo de audio
catalogo_escenarios = {
    "granja": {
        "titulo": "Animales de Granja",
        "descripcion": "Aprende lo que hacen los animales en el campo",
        "imagen_portada": "Animales de granja.jpg",
        "audio_descripcion": "desc_granja.mp3",
        "lista_escenarios": [
            {
                "texto_oracion": "El caballo come pasto",
                "audio_oracion": "oracion_granja_1.mp3",
                "etiquetas_casillas": ["SUJETO (¿Quién?)", "ACCIÓN (¿Qué hace?)", "COMPLEMENTO (¿Qué?)"],
                "objetivo": [
                    {"id": "caballo", "etiqueta": "CABALLO", "archivo": "Caballo.jpg", "categoria": "sujeto", "locucion": "Caballo", "audio_locucion": "pic_caballo.mp3"},
                    {"id": "come", "etiqueta": "COME", "archivo": "Comer.jpg", "categoria": "accion", "locucion": "Come", "audio_locucion": "pic_come.mp3"},
                    {"id": "pasto", "etiqueta": "PASTO", "archivo": "Pasto.jpg", "categoria": "complemento", "locucion": "Pasto", "audio_locucion": "pic_pasto.mp3"}
                ],
                "opciones": [
                    {"id": "pasto", "etiqueta": "PASTO", "archivo": "Pasto.jpg", "categoria": "complemento", "locucion": "Pasto", "audio_locucion": "pic_pasto.mp3"},
                    {"id": "caballo", "etiqueta": "CABALLO", "archivo": "Caballo.jpg", "categoria": "sujeto", "locucion": "Caballo", "audio_locucion": "pic_caballo.mp3"},
                    {"id": "come", "etiqueta": "COME", "archivo": "Comer.jpg", "categoria": "accion", "locucion": "Come", "audio_locucion": "pic_come.mp3"}
                ],
                "pistas": [
                    {"pregunta": "¿Quién realiza la acción?", "audio_pregunta": "pista_quien_realiza_la_accion.mp3", "archivo_ayuda": "Sujeto.png", "etiqueta_ayuda": "SUJETO (¿QUIÉN?)"},
                    {"pregunta": "¿Qué está haciendo el caballo?", "audio_pregunta": "pista_que_esta_haciendo_el_caballo.mp3", "archivo_ayuda": "Accion.png", "etiqueta_ayuda": "ACCIÓN (¿QUÉ HACE?)"},
                    {"pregunta": "¿Qué come el caballo?", "audio_pregunta": "pista_que_come_el_caballo.mp3", "archivo_ayuda": "Complemento.png", "etiqueta_ayuda": "COMPLEMENTO (¿QUÉ?)"}
                ]
            },
            {
                "texto_oracion": "El cerdo duerme en el barro",
                "audio_oracion": "oracion_granja_2.mp3",
                "etiquetas_casillas": ["SUJETO (¿Quién?)", "ACCIÓN (¿Qué hace?)", "COMPLEMENTO (¿Dónde?)"],
                "objetivo": [
                    {"id": "cerdo", "etiqueta": "CERDO", "archivo": "Cerdo.jpg", "categoria": "sujeto", "locucion": "Cerdo", "audio_locucion": "pic_cerdo.mp3"},
                    {"id": "duerme", "etiqueta": "DUERME", "archivo": "Dormir.jpg", "categoria": "accion", "locucion": "Duerme", "audio_locucion": "pic_duerme.mp3"},
                    {"id": "barro", "etiqueta": "BARRO", "archivo": "Barro.jpg", "categoria": "complemento", "locucion": "Barro", "audio_locucion": "pic_barro.mp3"}
                ],
                "opciones": [
                    {"id": "duerme", "etiqueta": "DUERME", "archivo": "Dormir.jpg", "categoria": "accion", "locucion": "Duerme", "audio_locucion": "pic_duerme.mp3"},
                    {"id": "barro", "etiqueta": "BARRO", "archivo": "Barro.jpg", "categoria": "complemento", "locucion": "Barro", "audio_locucion": "pic_barro.mp3"},
                    {"id": "cerdo", "etiqueta": "CERDO", "archivo": "Cerdo.jpg", "categoria": "sujeto", "locucion": "Cerdo", "audio_locucion": "pic_cerdo.mp3"}
                ],
                "pistas": [
                    {"pregunta": "¿Quién realiza la acción?", "audio_pregunta": "pista_quien_realiza_la_accion.mp3", "archivo_ayuda": "Sujeto.png", "etiqueta_ayuda": "SUJETO (¿QUIÉN?)"},
                    {"pregunta": "¿Qué está haciendo el cerdo?", "audio_pregunta": "pista_que_esta_haciendo_el_cerdo.mp3", "archivo_ayuda": "Accion.png", "etiqueta_ayuda": "ACCIÓN (¿QUÉ HACE?)"},
                    {"pregunta": "¿Dónde duerme el cerdo?", "audio_pregunta": "pista_donde_duerme_el_cerdo.mp3", "archivo_ayuda": "Complemento.png", "etiqueta_ayuda": "COMPLEMENTO (¿DÓNDE?)"}
                ]
            },
            {
                "texto_oracion": "La vaca corre en el corral",
                "audio_oracion": "oracion_granja_3.mp3",
                "etiquetas_casillas": ["SUJETO (¿Quién?)", "ACCIÓN (¿Qué hace?)", "COMPLEMENTO (¿Dónde?)"],
                "objetivo": [
                    {"id": "vaca", "etiqueta": "VACA", "archivo": "Vaca.jpg", "categoria": "sujeto", "locucion": "Vaca", "audio_locucion": "pic_vaca.mp3"},
                    {"id": "corre", "etiqueta": "CORRE", "archivo": "Correr.jpg", "categoria": "accion", "locucion": "Corre", "audio_locucion": "pic_corre.mp3"},
                    {"id": "corral", "etiqueta": "CORRAL", "archivo": "Corral.jpg", "categoria": "complemento", "locucion": "Corral", "audio_locucion": "pic_corral.mp3"}
                ],
                "opciones": [
                    {"id": "corral", "etiqueta": "CORRAL", "archivo": "Corral.jpg", "categoria": "complemento", "locucion": "Corral", "audio_locucion": "pic_corral.mp3"},
                    {"id": "vaca", "etiqueta": "VACA", "archivo": "Vaca.jpg", "categoria": "sujeto", "locucion": "Vaca", "audio_locucion": "pic_vaca.mp3"},
                    {"id": "corre", "etiqueta": "CORRE", "archivo": "Correr.jpg", "categoria": "accion", "locucion": "Corre", "audio_locucion": "pic_corre.mp3"}
                ],
                "pistas": [
                    {"pregunta": "¿Quién realiza la acción?", "audio_pregunta": "pista_quien_realiza_la_accion.mp3", "archivo_ayuda": "Sujeto.png", "etiqueta_ayuda": "SUJETO (¿QUIÉN?)"},
                    {"pregunta": "¿Qué está haciendo la vaca?", "audio_pregunta": "pista_que_esta_haciendo_la_vaca.mp3", "archivo_ayuda": "Accion.png", "etiqueta_ayuda": "ACCIÓN (¿QUÉ HACE?)"},
                    {"pregunta": "¿Dónde corre la vaca?", "audio_pregunta": "pista_donde_corre_la_vaca.mp3", "archivo_ayuda": "Complemento.png", "etiqueta_ayuda": "COMPLEMENTO (¿DÓNDE?)"}
                ]
            },
            {
                "texto_oracion": "El caballo corre en el pasto",
                "audio_oracion": "oracion_granja_4.mp3",
                "etiquetas_casillas": ["SUJETO (¿Quién?)", "ACCIÓN (¿Qué hace?)", "COMPLEMENTO (¿Dónde?)"],
                "objetivo": [
                    {"id": "caballo", "etiqueta": "CABALLO", "archivo": "Caballo.jpg", "categoria": "sujeto", "locucion": "Caballo", "audio_locucion": "pic_caballo.mp3"},
                    {"id": "corre", "etiqueta": "CORRE", "archivo": "Correr.jpg", "categoria": "accion", "locucion": "Corre", "audio_locucion": "pic_corre.mp3"},
                    {"id": "pasto", "etiqueta": "PASTO", "archivo": "Pasto.jpg", "categoria": "complemento", "locucion": "Pasto", "audio_locucion": "pic_pasto.mp3"}
                ],
                "opciones": [
                    {"id": "corre", "etiqueta": "CORRE", "archivo": "Correr.jpg", "categoria": "accion", "locucion": "Corre", "audio_locucion": "pic_corre.mp3"},
                    {"id": "pasto", "etiqueta": "PASTO", "archivo": "Pasto.jpg", "categoria": "complemento", "locucion": "Pasto", "audio_locucion": "pic_pasto.mp3"},
                    {"id": "caballo", "etiqueta": "CABALLO", "archivo": "Caballo.jpg", "categoria": "sujeto", "locucion": "Caballo", "audio_locucion": "pic_caballo.mp3"}
                ],
                "pistas": [
                    {"pregunta": "¿Quién realiza la acción?", "audio_pregunta": "pista_quien_realiza_la_accion.mp3", "archivo_ayuda": "Sujeto.png", "etiqueta_ayuda": "SUJETO (¿QUIÉN?)"},
                    {"pregunta": "¿Qué está haciendo el caballo?", "audio_pregunta": "pista_que_esta_haciendo_el_caballo.mp3", "archivo_ayuda": "Accion.png", "etiqueta_ayuda": "ACCIÓN (¿QUÉ HACE?)"},
                    {"pregunta": "¿Dónde corre el caballo?", "audio_pregunta": "pista_donde_corre_el_caballo.mp3", "archivo_ayuda": "Complemento.png", "etiqueta_ayuda": "COMPLEMENTO (¿DÓNDE?)"}
                ]
            },
            {
                "texto_oracion": "La vaca come pasto",
                "audio_oracion": "oracion_granja_5.mp3",
                "etiquetas_casillas": ["SUJETO (¿Quién?)", "ACCIÓN (¿Qué hace?)", "COMPLEMENTO (¿Qué?)"],
                "objetivo": [
                    {"id": "vaca", "etiqueta": "VACA", "archivo": "Vaca.jpg", "categoria": "sujeto", "locucion": "Vaca", "audio_locucion": "pic_vaca.mp3"},
                    {"id": "come", "etiqueta": "COME", "archivo": "Comer.jpg", "categoria": "accion", "locucion": "Come", "audio_locucion": "pic_come.mp3"},
                    {"id": "pasto", "etiqueta": "PASTO", "archivo": "Pasto.jpg", "categoria": "complemento", "locucion": "Pasto", "audio_locucion": "pic_pasto.mp3"}
                ],
                "opciones": [
                    {"id": "pasto", "etiqueta": "PASTO", "archivo": "Pasto.jpg", "categoria": "complemento", "locucion": "Pasto", "audio_locucion": "pic_pasto.mp3"},
                    {"id": "come", "etiqueta": "COME", "archivo": "Comer.jpg", "categoria": "accion", "locucion": "Come", "audio_locucion": "pic_come.mp3"},
                    {"id": "vaca", "etiqueta": "VACA", "archivo": "Vaca.jpg", "categoria": "sujeto", "locucion": "Vaca", "audio_locucion": "pic_vaca.mp3"}
                ],
                "pistas": [
                    {"pregunta": "¿Quién realiza la acción?", "audio_pregunta": "pista_quien_realiza_la_accion.mp3", "archivo_ayuda": "Sujeto.png", "etiqueta_ayuda": "SUJETO (¿QUIÉN?)"},
                    {"pregunta": "¿Qué está haciendo la vaca?", "audio_pregunta": "pista_que_esta_haciendo_la_vaca.mp3", "archivo_ayuda": "Accion.png", "etiqueta_ayuda": "ACCIÓN (¿QUÉ HACE?)"},
                    {"pregunta": "¿Qué come la vaca?", "audio_pregunta": "pista_que_come_la_vaca.mp3", "archivo_ayuda": "Complemento.png", "etiqueta_ayuda": "COMPLEMENTO (¿QUÉ?)"}
                ]
            }
        ]
    },
    "rutinas": {
        "titulo": "Rutinas Diarias",
        "descripcion": "Momentos cotidianos de alimentación en casa",
        "imagen_portada": "Rutinas diarias.jpg",
        "audio_descripcion": "desc_rutinas.mp3",
        "lista_escenarios": [
            {
                "texto_oracion": "El niño bebe jugo de naranja",
                "audio_oracion": "oracion_rutinas_1.mp3",
                "etiquetas_casillas": ["SUJETO (¿Quién?)", "ACCIÓN (¿Qué hace?)", "COMPLEMENTO (¿Qué?)"],
                "objetivo": [
                    {"id": "nino", "etiqueta": "NIÑO", "archivo": "Niño.jpg", "categoria": "sujeto", "locucion": "Niño", "audio_locucion": "pic_nino.mp3"},
                    {"id": "bebe", "etiqueta": "BEBE", "archivo": "Beber.jpg", "categoria": "accion", "locucion": "Bebe", "audio_locucion": "pic_bebe.mp3"},
                    {"id": "jugo", "etiqueta": "JUGO", "archivo": "Jugo de naranja.jpg", "categoria": "complemento", "locucion": "Jugo de naranja", "audio_locucion": "pic_jugo.mp3"}
                ],
                "opciones": [
                    {"id": "jugo", "etiqueta": "JUGO", "archivo": "Jugo de naranja.jpg", "categoria": "complemento", "locucion": "Jugo de naranja", "audio_locucion": "pic_jugo.mp3"},
                    {"id": "nino", "etiqueta": "NIÑO", "archivo": "Niño.jpg", "categoria": "sujeto", "locucion": "Niño", "audio_locucion": "pic_nino.mp3"},
                    {"id": "bebe", "etiqueta": "BEBE", "archivo": "Beber.jpg", "categoria": "accion", "locucion": "Bebe", "audio_locucion": "pic_bebe.mp3"}
                ],
                "pistas": [
                    {"pregunta": "¿Quién realiza la acción?", "audio_pregunta": "pista_quien_realiza_la_accion.mp3", "archivo_ayuda": "Sujeto.png", "etiqueta_ayuda": "SUJETO (¿QUIÉN?)"},
                    {"pregunta": "¿Qué está haciendo el niño?", "audio_pregunta": "pista_que_esta_haciendo_el_nino.mp3", "archivo_ayuda": "Accion.png", "etiqueta_ayuda": "ACCIÓN (¿QUÉ HACE?)"},
                    {"pregunta": "¿Qué toma el niño?", "audio_pregunta": "pista_que_toma_el_nino.mp3", "archivo_ayuda": "Complemento.png", "etiqueta_ayuda": "COMPLEMENTO (¿QUÉ?)"}
                ]
            },
            {
                "texto_oracion": "La niña juega con la pelota",
                "audio_oracion": "oracion_rutinas_2.mp3",
                "etiquetas_casillas": ["SUJETO (¿Quién?)", "ACCIÓN (¿Qué hace?)", "COMPLEMENTO (¿Con qué?)"],
                "objetivo": [
                    {"id": "nina", "etiqueta": "NIÑA", "archivo": "Niña.jpg", "categoria": "sujeto", "locucion": "Niña", "audio_locucion": "pic_nina.mp3"},
                    {"id": "juega", "etiqueta": "JUEGA", "archivo": "Jugar.jpg", "categoria": "accion", "locucion": "Juega", "audio_locucion": "pic_juega.mp3"},
                    {"id": "pelota", "etiqueta": "PELOTA", "archivo": "Pelota.jpg", "categoria": "complemento", "locucion": "Pelota", "audio_locucion": "pic_pelota.mp3"}
                ],
                "opciones": [
                    {"id": "pelota", "etiqueta": "PELOTA", "archivo": "Pelota.jpg", "categoria": "complemento", "locucion": "Pelota", "audio_locucion": "pic_pelota.mp3"},
                    {"id": "nina", "etiqueta": "NIÑA", "archivo": "Niña.jpg", "categoria": "sujeto", "locucion": "Niña", "audio_locucion": "pic_nina.mp3"},
                    {"id": "juega", "etiqueta": "JUEGA", "archivo": "Jugar.jpg", "categoria": "accion", "locucion": "Juega", "audio_locucion": "pic_juega.mp3"}
                ],
                "pistas": [
                    {"pregunta": "¿Quién realiza la acción?", "audio_pregunta": "pista_quien_realiza_la_accion.mp3", "archivo_ayuda": "Sujeto.png", "etiqueta_ayuda": "SUJETO (¿QUIÉN?)"},
                    {"pregunta": "¿Qué está haciendo la niña?", "audio_pregunta": "pista_que_esta_haciendo_la_nina.mp3", "archivo_ayuda": "Accion.png", "etiqueta_ayuda": "ACCIÓN (¿QUÉ HACE?)"},
                    {"pregunta": "¿Con qué juega la niña?", "audio_pregunta": "pista_con_que_juega_la_nina.mp3", "archivo_ayuda": "Complemento.png", "etiqueta_ayuda": "COMPLEMENTO (¿CON QUÉ?)"}
                ]
            },
            {
                "texto_oracion": "Mamá e hijo leen un libro",
                "audio_oracion": "oracion_rutinas_3.mp3",
                "etiquetas_casillas": ["SUJETO (¿Quiénes?)", "ACCIÓN (¿Qué hacen?)", "COMPLEMENTO (¿Qué?)"],
                "objetivo": [
                    {"id": "mama_hijo", "etiqueta": "MAMÁ E HIJO", "archivo": "Mamá e hijo.jpg", "categoria": "sujeto", "locucion": "Mamá e hijo", "audio_locucion": "pic_mama_hijo.mp3"},
                    {"id": "leen", "etiqueta": "LEEN", "archivo": "Leer.jpg", "categoria": "accion", "locucion": "Leen", "audio_locucion": "pic_leen.mp3"},
                    {"id": "libro", "etiqueta": "LIBRO", "archivo": "Libro.jpg", "categoria": "complemento", "locucion": "Libro", "audio_locucion": "pic_libro.mp3"}
                ],
                "opciones": [
                    {"id": "libro", "etiqueta": "LIBRO", "archivo": "Libro.jpg", "categoria": "complemento", "locucion": "Libro", "audio_locucion": "pic_libro.mp3"},
                    {"id": "mama_hijo", "etiqueta": "MAMÁ E HIJO", "archivo": "Mamá e hijo.jpg", "categoria": "sujeto", "locucion": "Mamá e hijo", "audio_locucion": "pic_mama_hijo.mp3"},
                    {"id": "leen", "etiqueta": "LEEN", "archivo": "Leer.jpg", "categoria": "accion", "locucion": "Leen", "audio_locucion": "pic_leen.mp3"}
                ],
                "pistas": [
                    {"pregunta": "¿Quiénes realizan la acción?", "audio_pregunta": "pista_quien_realiza_la_accion.mp3", "archivo_ayuda": "Sujeto.png", "etiqueta_ayuda": "SUJETO (¿QUIÉNES?)"},
                    {"pregunta": "¿Qué están haciendo mamá e hijo?", "audio_pregunta": "pista_que_estan_haciendo_mama_e_hijo.mp3", "archivo_ayuda": "Accion.png", "etiqueta_ayuda": "ACCIÓN (¿QUÉ HACEN?)"},
                    {"pregunta": "¿Qué leen juntos?", "audio_pregunta": "pista_que_leen_juntos.mp3", "archivo_ayuda": "Complemento.png", "etiqueta_ayuda": "COMPLEMENTO (¿QUÉ?)"}
                ]
            },
            {
                "texto_oracion": "Papá e hijo juegan con la pelota",
                "audio_oracion": "oracion_rutinas_4.mp3",
                "etiquetas_casillas": ["SUJETO (¿Quiénes?)", "ACCIÓN (¿Qué hacen?)", "COMPLEMENTO (¿Con qué?)"],
                "objetivo": [
                    {"id": "papa_hijo", "etiqueta": "PAPÁ E HIJO", "archivo": "Papá e hijo.jpg", "categoria": "sujeto", "locucion": "Papá e hijo", "audio_locucion": "pic_papa_hijo.mp3"},
                    {"id": "juegan", "etiqueta": "JUEGAN", "archivo": "Jugar.jpg", "categoria": "accion", "locucion": "Juegan", "audio_locucion": "pic_juegan.mp3"},
                    {"id": "pelota", "etiqueta": "PELOTA", "archivo": "Pelota.jpg", "categoria": "complemento", "locucion": "Pelota", "audio_locucion": "pic_pelota.mp3"}
                ],
                "opciones": [
                    {"id": "papa_hijo", "etiqueta": "PAPÁ E HIJO", "archivo": "Papá e hijo.jpg", "categoria": "sujeto", "locucion": "Papá e hijo", "audio_locucion": "pic_papa_hijo.mp3"},
                    {"id": "pelota", "etiqueta": "PELOTA", "archivo": "Pelota.jpg", "categoria": "complemento", "locucion": "Pelota", "audio_locucion": "pic_pelota.mp3"},
                    {"id": "juegan", "etiqueta": "JUEGAN", "archivo": "Jugar.jpg", "categoria": "accion", "locucion": "Juegan", "audio_locucion": "pic_juegan.mp3"}
                ],
                "pistas": [
                    {"pregunta": "¿Quiénes realizan la acción?", "audio_pregunta": "pista_quien_realiza_la_accion.mp3", "archivo_ayuda": "Sujeto.png", "etiqueta_ayuda": "SUJETO (¿QUIÉNES?)"},
                    {"pregunta": "¿Qué están haciendo papá e hijo?", "audio_pregunta": "pista_que_estan_haciendo_papa_e_hijo.mp3", "archivo_ayuda": "Accion.png", "etiqueta_ayuda": "ACCIÓN (¿QUÉ HACEN?)"},
                    {"pregunta": "¿Con qué juegan?", "audio_pregunta": "pista_con_que_juegan.mp3", "archivo_ayuda": "Complemento.png", "etiqueta_ayuda": "COMPLEMENTO (¿CON QUÉ?)"}
                ]
            },
            {
                "texto_oracion": "La niña lee un libro",
                "audio_oracion": "oracion_rutinas_5.mp3",
                "etiquetas_casillas": ["SUJETO (¿Quién?)", "ACCIÓN (¿Qué hace?)", "COMPLEMENTO (¿Qué?)"],
                "objetivo": [
                    {"id": "nina", "etiqueta": "NIÑA", "archivo": "Niña.jpg", "categoria": "sujeto", "locucion": "Niña", "audio_locucion": "pic_nina.mp3"},
                    {"id": "lee", "etiqueta": "LEE", "archivo": "Leer.jpg", "categoria": "accion", "locucion": "Lee", "audio_locucion": "pic_lee.mp3"},
                    {"id": "libro", "etiqueta": "LIBRO", "archivo": "Libro.jpg", "categoria": "complemento", "locucion": "Libro", "audio_locucion": "pic_libro.mp3"}
                ],
                "opciones": [
                    {"id": "lee", "etiqueta": "LEE", "archivo": "Leer.jpg", "categoria": "accion", "locucion": "Lee", "audio_locucion": "pic_lee.mp3"},
                    {"id": "libro", "etiqueta": "LIBRO", "archivo": "Libro.jpg", "categoria": "complemento", "locucion": "Libro", "audio_locucion": "pic_libro.mp3"},
                    {"id": "nina", "etiqueta": "NIÑA", "archivo": "Niña.jpg", "categoria": "sujeto", "locucion": "Niña", "audio_locucion": "pic_nina.mp3"}
                ],
                "pistas": [
                    {"pregunta": "¿Quién realiza la acción?", "audio_pregunta": "pista_quien_realiza_la_accion.mp3", "archivo_ayuda": "Sujeto.png", "etiqueta_ayuda": "SUJETO (¿QUIÉN?)"},
                    {"pregunta": "¿Qué está haciendo la niña?", "audio_pregunta": "pista_que_esta_haciendo_la_nina.mp3", "archivo_ayuda": "Accion.png", "etiqueta_ayuda": "ACCIÓN (¿QUÉ HACE?)"},
                    {"pregunta": "¿Qué lee la niña?", "audio_pregunta": "pista_que_lee_la_nina.mp3", "archivo_ayuda": "Complemento.png", "etiqueta_ayuda": "COMPLEMENTO (¿QUÉ?)"}
                ]
            }
        ]
    },
    "aseo": {
        "titulo": "Aseo Personal",
        "descripcion": "Hábitos de higiene y cuidado saludable",
        "imagen_portada": "Aseo personal.jpg",
        "audio_descripcion": "desc_aseo.mp3",
        "lista_escenarios": [
            {
                "texto_oracion": "La niña lava sus manos",
                "audio_oracion": "oracion_aseo_1.mp3",
                "etiquetas_casillas": ["SUJETO (¿Quién?)", "ACCIÓN (¿Qué hace?)", "COMPLEMENTO (¿Qué?)"],
                "objetivo": [
                    {"id": "nina", "etiqueta": "NIÑA", "archivo": "Niña.jpg", "categoria": "sujeto", "locucion": "Niña", "audio_locucion": "pic_nina.mp3"},
                    {"id": "lava", "etiqueta": "LAVA", "archivo": "Lavarse las manos.jpg", "categoria": "accion", "locucion": "Lava", "audio_locucion": "pic_lava.mp3"},
                    {"id": "manos", "etiqueta": "MANOS", "archivo": "Manos.jpg", "categoria": "complemento", "locucion": "Manos", "audio_locucion": "pic_manos.mp3"}
                ],
                "opciones": [
                    {"id": "manos", "etiqueta": "MANOS", "archivo": "Manos.jpg", "categoria": "complemento", "locucion": "Manos", "audio_locucion": "pic_manos.mp3"},
                    {"id": "lava", "etiqueta": "LAVA", "archivo": "Lavarse las manos.jpg", "categoria": "accion", "locucion": "Lava", "audio_locucion": "pic_lava.mp3"},
                    {"id": "nina", "etiqueta": "NIÑA", "archivo": "Niña.jpg", "categoria": "sujeto", "locucion": "Niña", "audio_locucion": "pic_nina.mp3"}
                ],
                "pistas": [
                    {"pregunta": "¿Quién realiza la acción?", "audio_pregunta": "pista_quien_realiza_la_accion.mp3", "archivo_ayuda": "Sujeto.png", "etiqueta_ayuda": "SUJETO (¿QUIÉN?)"},
                    {"pregunta": "¿Qué está haciendo la niña?", "audio_pregunta": "pista_que_esta_haciendo_la_nina.mp3", "archivo_ayuda": "Accion.png", "etiqueta_ayuda": "ACCIÓN (¿QUÉ HACE?)"},
                    {"pregunta": "¿Qué se lava la niña?", "audio_pregunta": "pista_que_se_lava_la_nina.mp3", "archivo_ayuda": "Complemento.png", "etiqueta_ayuda": "COMPLEMENTO (¿QUÉ?)"}
                ]
            },
            {
                "texto_oracion": "El niño cepilla su boca",
                "audio_oracion": "oracion_aseo_2.mp3",
                "etiquetas_casillas": ["SUJETO (¿Quién?)", "ACCIÓN (¿Qué hace?)", "COMPLEMENTO (¿Qué parte?)"],
                "objetivo": [
                    {"id": "nino", "etiqueta": "NIÑO", "archivo": "Niño.jpg", "categoria": "sujeto", "locucion": "Niño", "audio_locucion": "pic_nino.mp3"},
                    {"id": "cepilla", "etiqueta": "CEPILLA", "archivo": "Cepillarse los dientes.jpg", "categoria": "accion", "locucion": "Cepilla", "audio_locucion": "pic_cepilla.mp3"},
                    {"id": "boca", "etiqueta": "BOCA", "archivo": "Boca.jpg", "categoria": "complemento", "locucion": "Boca", "audio_locucion": "pic_boca.mp3"}
                ],
                "opciones": [
                    {"id": "cepilla", "etiqueta": "CEPILLA", "archivo": "Cepillarse los dientes.jpg", "categoria": "accion", "locucion": "Cepilla", "audio_locucion": "pic_cepilla.mp3"},
                    {"id": "boca", "etiqueta": "BOCA", "archivo": "Boca.jpg", "categoria": "complemento", "locucion": "Boca", "audio_locucion": "pic_boca.mp3"},
                    {"id": "nino", "etiqueta": "NIÑO", "archivo": "Niño.jpg", "categoria": "sujeto", "locucion": "Niño", "audio_locucion": "pic_nino.mp3"}
                ],
                "pistas": [
                    {"pregunta": "¿Quién realiza la acción?", "audio_pregunta": "pista_quien_realiza_la_accion.mp3", "archivo_ayuda": "Sujeto.png", "etiqueta_ayuda": "SUJETO (¿QUIÉN?)"},
                    {"pregunta": "¿Qué está haciendo el niño?", "audio_pregunta": "pista_que_esta_haciendo_el_nino.mp3", "archivo_ayuda": "Accion.png", "etiqueta_ayuda": "ACCIÓN (¿QUÉ HACE?)"},
                    {"pregunta": "¿Qué parte se cepilla?", "audio_pregunta": "pista_que_parte_se_cepilla.mp3", "archivo_ayuda": "Complemento.png", "etiqueta_ayuda": "COMPLEMENTO (¿QUÉ PARTE?)"}
                ]
            },
            {
                "texto_oracion": "La niña peina su pelo",
                "audio_oracion": "oracion_aseo_3.mp3",
                "etiquetas_casillas": ["SUJETO (¿Quién?)", "ACCIÓN (¿Qué hace?)", "COMPLEMENTO (¿Qué parte?)"],
                "objetivo": [
                    {"id": "nina", "etiqueta": "NIÑA", "archivo": "Niña.jpg", "categoria": "sujeto", "locucion": "Niña", "audio_locucion": "pic_nina.mp3"},
                    {"id": "peina", "etiqueta": "PEINA", "archivo": "Peinarse.jpg", "categoria": "accion", "locucion": "Peina", "audio_locucion": "pic_peina.mp3"},
                    {"id": "pelo", "etiqueta": "PELO", "archivo": "Pelo.jpg", "categoria": "complemento", "locucion": "Pelo", "audio_locucion": "pic_pelo.mp3"}
                ],
                "opciones": [
                    {"id": "pelo", "etiqueta": "PELO", "archivo": "Pelo.jpg", "categoria": "complemento", "locucion": "Pelo", "audio_locucion": "pic_pelo.mp3"},
                    {"id": "peina", "etiqueta": "PEINA", "archivo": "Peinarse.jpg", "categoria": "accion", "locucion": "Peina", "audio_locucion": "pic_peina.mp3"},
                    {"id": "nina", "etiqueta": "NIÑA", "archivo": "Niña.jpg", "categoria": "sujeto", "locucion": "Niña", "audio_locucion": "pic_nina.mp3"}
                ],
                "pistas": [
                    {"pregunta": "¿Quién realiza la acción?", "audio_pregunta": "pista_quien_realiza_la_accion.mp3", "archivo_ayuda": "Sujeto.png", "etiqueta_ayuda": "SUJETO (¿QUIÉN?)"},
                    {"pregunta": "¿Qué está haciendo la niña?", "audio_pregunta": "pista_que_esta_haciendo_la_nina.mp3", "archivo_ayuda": "Accion.png", "etiqueta_ayuda": "ACCIÓN (¿QUÉ HACE?)"},
                    {"pregunta": "¿Qué se peina la niña?", "audio_pregunta": "pista_que_se_peina_la_nina.mp3", "archivo_ayuda": "Complemento.png", "etiqueta_ayuda": "COMPLEMENTO (¿QUÉ PARTE?)"}
                ]
            },
            {
                "texto_oracion": "El niño seca sus manos",
                "audio_oracion": "oracion_aseo_4.mp3",
                "etiquetas_casillas": ["SUJETO (¿Quién?)", "ACCIÓN (¿Qué hace?)", "COMPLEMENTO (¿Qué?)"],
                "objetivo": [
                    {"id": "nino", "etiqueta": "NIÑO", "archivo": "Niño.jpg", "categoria": "sujeto", "locucion": "Niño", "audio_locucion": "pic_nino.mp3"},
                    {"id": "seca", "etiqueta": "SECA", "archivo": "Secarse las manos.jpg", "categoria": "accion", "locucion": "Seca", "audio_locucion": "pic_seca.mp3"},
                    {"id": "manos", "etiqueta": "MANOS", "archivo": "Manos.jpg", "categoria": "complemento", "locucion": "Manos", "audio_locucion": "pic_manos.mp3"}
                ],
                "opciones": [
                    {"id": "manos", "etiqueta": "MANOS", "archivo": "Manos.jpg", "categoria": "complemento", "locucion": "Manos", "audio_locucion": "pic_manos.mp3"},
                    {"id": "nino", "etiqueta": "NIÑO", "archivo": "Niño.jpg", "categoria": "sujeto", "locucion": "Niño", "audio_locucion": "pic_nino.mp3"},
                    {"id": "seca", "etiqueta": "SECA", "archivo": "Secarse las manos.jpg", "categoria": "accion", "locucion": "Seca", "audio_locucion": "pic_seca.mp3"}
                ],
                "pistas": [
                    {"pregunta": "¿Quién realiza la acción?", "audio_pregunta": "pista_quien_realiza_la_accion.mp3", "archivo_ayuda": "Sujeto.png", "etiqueta_ayuda": "SUJETO (¿QUIÉN?)"},
                    {"pregunta": "¿Qué está haciendo el niño?", "audio_pregunta": "pista_que_esta_haciendo_el_nino.mp3", "archivo_ayuda": "Accion.png", "etiqueta_ayuda": "ACCIÓN (¿QUÉ HACE?)"},
                    {"pregunta": "¿Qué se seca el niño?", "audio_pregunta": "pista_que_se_lava_la_nina.mp3", "archivo_ayuda": "Complemento.png", "etiqueta_ayuda": "COMPLEMENTO (¿QUÉ?)"}
                ]
            },
            {
                "texto_oracion": "La niña lava su cara",
                "audio_oracion": "oracion_aseo_5.mp3",
                "etiquetas_casillas": ["SUJETO (¿Quién?)", "ACCIÓN (¿Qué hace?)", "COMPLEMENTO (¿Qué parte?)"],
                "objetivo": [
                    {"id": "nina", "etiqueta": "NIÑA", "archivo": "Niña.jpg", "categoria": "sujeto", "locucion": "Niña", "audio_locucion": "pic_nina.mp3"},
                    {"id": "lava", "etiqueta": "LAVA", "archivo": "Lavarse las manos.jpg", "categoria": "accion", "locucion": "Lava", "audio_locucion": "pic_lava.mp3"},
                    {"id": "cara", "etiqueta": "CARA", "archivo": "Cara.jpg", "categoria": "complemento", "locucion": "Cara", "audio_locucion": "pic_cara.mp3"}
                ],
                "opciones": [
                    {"id": "cara", "etiqueta": "CARA", "archivo": "Cara.jpg", "categoria": "complemento", "locucion": "Cara", "audio_locucion": "pic_cara.mp3"},
                    {"id": "lava", "etiqueta": "LAVA", "archivo": "Lavarse las manos.jpg", "categoria": "accion", "locucion": "Lava", "audio_locucion": "pic_lava.mp3"},
                    {"id": "nina", "etiqueta": "NIÑA", "archivo": "Niña.jpg", "categoria": "sujeto", "locucion": "Niña", "audio_locucion": "pic_nina.mp3"}
                ],
                "pistas": [
                    {"pregunta": "¿Quién realiza la acción?", "audio_pregunta": "pista_quien_realiza_la_accion.mp3", "archivo_ayuda": "Sujeto.png", "etiqueta_ayuda": "SUJETO (¿QUIÉN?)"},
                    {"pregunta": "¿Qué está haciendo la niña?", "audio_pregunta": "pista_que_esta_haciendo_la_nina.mp3", "archivo_ayuda": "Accion.png", "etiqueta_ayuda": "ACCIÓN (¿QUÉ HACE?)"},
                    {"pregunta": "¿Qué se lava la niña?", "audio_pregunta": "pista_que_se_lava_la_nina.mp3", "archivo_ayuda": "Complemento.png", "etiqueta_ayuda": "COMPLEMENTO (¿QUÉ PARTE?)"}
                ]
            }
        ]
    }
}

# catalogo estructurado de audios de interfaz navegacion y turnos
catalogo_audios_interfaz = {
    "bienvenida": "ui_bienvenida.mp3",
    "boton_ayuda": "ui_boton_ayuda.mp3",
    "felicitacion_final": "ui_felicitacion_final.mp3",
    "jugadores": {
        1: "ui_jugador_1.mp3",
        2: "ui_jugador_2.mp3",
        3: "ui_jugador_3.mp3",
        4: "ui_jugador_4.mp3"
    },
    "turnos": {
        1: "turno_j1.mp3",
        2: "turno_j2.mp3",
        3: "turno_j3.mp3",
        4: "turno_j4.mp3"
    }
}
