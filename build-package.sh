#!/bin/bash

# RadLog Download Package Builder
# Creates a zip file ready for Lemon Squeezy

set -e

echo "🏥 Building RadLog Download Package..."

# Create package directory
PACKAGE_DIR="radlog-package"
ZIP_FILE="RadLog-v1.0.0.zip"

# Clean and create package directory
rm -rf "$PACKAGE_DIR"
mkdir "$PACKAGE_DIR"

echo "📦 Copying files..."

# Copy main executable (assuming it exists)
if [ -f "app/RadLog.exe" ]; then
    cp "app/RadLog.exe" "$PACKAGE_DIR/"
    echo "✅ RadLog.exe copied"
else
    echo "⚠️ Warning: RadLog.exe not found in app/ directory"
    echo "   You'll need to build the Windows app first"
fi

# Copy documentation
cp "download-package/README.txt" "$PACKAGE_DIR/"
cp "download-package/安裝指南.md" "$PACKAGE_DIR/"
cp "download-package/LICENSE.txt" "$PACKAGE_DIR/"

# Convert Markdown to PDF (if pandoc is available)
if command -v pandoc &> /dev/null; then
    echo "📄 Converting installation guide to PDF..."
    pandoc "download-package/安裝指南.md" \
        --pdf-engine=xelatex \
        --variable mainfont="PingFang TC" \
        -o "$PACKAGE_DIR/安裝指南.pdf"
    echo "✅ 安裝指南.pdf created"
else
    echo "⚠️ pandoc not available - PDF conversion skipped"
    echo "   Consider installing pandoc for better documentation"
fi

# Create zip file
echo "🗜️ Creating zip package..."
zip -r "$ZIP_FILE" "$PACKAGE_DIR"

# Cleanup
rm -rf "$PACKAGE_DIR"

echo "✅ Package created: $ZIP_FILE"
echo "📊 Package size: $(ls -lh $ZIP_FILE | awk '{print $5}')"
echo ""
echo "🚀 Ready for Lemon Squeezy upload!"
echo ""
echo "📋 Upload checklist:"
echo "   □ Upload $ZIP_FILE to Lemon Squeezy"
echo "   □ Set price to \$19.99"
echo "   □ Configure webhook URL"
echo "   □ Test purchase flow"
echo "   □ Go live!"