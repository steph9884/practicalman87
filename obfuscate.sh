#!/bin/bash
# URL Obfuscation Tool Launcher
# =============================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

show_help() {
    echo "URL Obfuscation Tool Launcher"
    echo "============================="
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  single    Generate single URL(s) - default"
    echo "  batch     Batch process CSV/JSON files"
    echo "  server    Start web interface"
    echo "  help      Show this help"
    echo ""
    echo "Quick Examples:"
    echo "  $0 --email user@test.com --domain mysite.com"
    echo "  $0 --template admin_portal --email admin@corp.com --count 5"
    echo "  $0 batch --csv input.csv --template webmail_style"
    echo "  $0 server --port 8080"
    echo ""
    echo "For detailed options, run:"
    echo "  $0 single --help"
    echo "  $0 batch --help"
    echo "  $0 server --help"
}

case "$1" in
    "single")
        shift
        python3 "$SCRIPT_DIR/url_obfuscator.py" "$@"
        ;;
    "batch")
        shift
        python3 "$SCRIPT_DIR/batch_obfuscate.py" "$@"
        ;;
    "server")
        shift
        python3 "$SCRIPT_DIR/obfuscation_server.py" "$@"
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    "")
        echo "No command provided. Run '$0 help' for usage information."
        exit 1
        ;;
    --*)
        # If it starts with --, assume it's for the single command
        python3 "$SCRIPT_DIR/url_obfuscator.py" "$@"
        ;;
    *)
        echo "Unknown command: $1"
        echo "Run '$0 help' for usage information."
        exit 1
        ;;
esac