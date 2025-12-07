def migliora_grafica_app(chat_tab):
    chat_tab.output.append("[PLUGIN] Grafica evoluta 3D applicata!")
    try:
        # Esempio: cambia tema, aggiungi effetti 3D (placeholder)
        chat_tab.setStyleSheet("background-color: #181c20; color: #e1e1e1;")
        chat_tab.output.setStyleSheet("background-color: #10141a; color: #e1e1e1; font-size: 16px; border: 2px solid #00eaff; border-radius: 10px;")
        chat_tab.input.setStyleSheet("background-color: #23272e; color: #e1e1e1; border: 2px solid #00eaff; border-radius: 10px;")
        # Placeholder per effetti 3D: in una vera app PyQt5, qui si integrerebbero QGraphicsView/QOpenGLWidget
        chat_tab.output.append("[PLUGIN] Effetti 3D simulati: bordo luminoso e profondità.")
    except Exception as e:
        chat_tab.output.append(f"[PLUGIN] Errore tema 3D: {e}")
