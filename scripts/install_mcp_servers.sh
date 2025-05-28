#!/bin/bash

echo "🚀 Installing Invopop Expert MCP Servers..."

# Check if npm/npx is available
if ! command -v npx &> /dev/null; then
    echo "❌ Error: npx is not installed. Please install Node.js first."
    echo "Visit: https://nodejs.org/"
    exit 1
fi

echo "📦 Installing Invopop MCP server..."
npx mint-mcp add invopop

echo "📦 Installing GOBL MCP server..."  
npx mint-mcp add gobl

echo "✅ MCP servers installed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Copy .env.example to .env and add your OpenAI API key"
echo "2. Run: invopop-expert"