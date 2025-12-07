# Integrazione AI per Super Agent Workspace

def start_workspace():
    from super_agent_workspace.core.workspace_app import SuperAgentWorkspace
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    win = SuperAgentWorkspace()
    win.show()
    sys.exit(app.exec_())
