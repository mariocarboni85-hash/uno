"""Runner for custom agent: creatore"""
from agent import SuperAgent
from tools import shell, files, browser

TOOLS = {
    'shell': shell.run,
    'files_write': files.write_file,
    'files_read': files.read_file,
    'list_dir': files.list_dir,
    'browser': browser.fetch,
}


def main():
    agent = SuperAgent(TOOLS, name="creatore")
    print("Agente custom pronto. Integrazione specifica da completare.")


if __name__ == '__main__':
    main()
