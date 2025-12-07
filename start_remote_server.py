"""
Start Remote Super Agent Server
"""

from remote_server import RemoteSuperAgentServer
import sys


def main():
    """Start server"""
    
    print("=" * 80)
    print("REMOTE SUPER AGENT SERVER")
    print("=" * 80)
    
    # Get port from args
    port = 5000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port: {sys.argv[1]}, using default 5000")
    
    # Create and start server
    server = RemoteSuperAgentServer(port=port)
    
    print(f"\n[*] Server Configuration:")
    print(f"    Host: 0.0.0.0")
    print(f"    Port: {port}")
    print(f"    API Base: http://localhost:{port}/api")
    
    print(f"\n[*] Available Endpoints:")
    print(f"    GET  /api/health              - Health check")
    print(f"    POST /api/login               - Login (get JWT token)")
    print(f"    POST /api/tasks               - Create task")
    print(f"    GET  /api/tasks/<id>          - Get task status")
    print(f"    GET  /api/tasks               - List all tasks")
    print(f"    DELETE /api/tasks/<id>        - Delete task")
    print(f"    GET  /api/stats               - Server statistics")
    print(f"    POST /api/agent/code          - Generate code")
    print(f"    POST /api/agent/analyze       - Analyze code")
    print(f"    POST /api/agent/refactor      - Refactor code")
    print(f"    POST /api/agent/neural/predict - Neural prediction")
    print(f"    GET  /api/stream              - Real-time updates (SSE)")
    
    print(f"\n[*] Test Users:")
    print(f"    admin / admin123")
    print(f"    user / user123")
    
    print(f"\n[*] Client Usage:")
    print(f"    python demo_remote_client.py")
    print(f"    python remote_client.py")
    
    print(f"\n[*] Starting server...\n")
    
    try:
        server.run(debug=False)
    except KeyboardInterrupt:
        print("\n\n[*] Server stopped by user")
    except Exception as e:
        print(f"\n[ERROR] Server error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
