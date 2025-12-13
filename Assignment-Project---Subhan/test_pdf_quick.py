"""
Quick PDF Test Script
Tests PDF generation without running full analysis (saves 20-25 minutes!)
Run: python test_pdf_quick.py
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import the PDF generation function
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import from app module
try:
    from app import markdown_to_pdf
except ImportError:
    print("❌ Error: Could not import markdown_to_pdf from app.py")
    print("   Make sure app.py is in the same directory")
    sys.exit(1)
from datetime import datetime


def test_pdf_generation():
    """Test PDF generation with sample report."""
    print("🧪 Testing PDF Generation...")
    print("=" * 60)
    
    # Sample report content (similar to real analysis)
    sample_report = """# Apple Inc. (AAPL) - Business Analysis Report

## Executive Summary
Apple Inc. is a leading technology company with strong financial performance and market leadership. The company demonstrates consistent growth, innovation, and strong brand value. This analysis provides a comprehensive overview of Apple's financial health, competitive position, and investment potential.

## Company Overview
Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. The company operates through iPhone, Mac, iPad, Wearables, Home and Accessories, and Services segments.

**Key Statistics:**
- Market Cap: $2.8 Trillion
- Sector: Technology
- Industry: Consumer Electronics
- Employees: 164,000+

## Financial Analysis

### Stock Performance
- Current Price: $175.50
- 52-Week High: $198.23
- 52-Week Low: $164.08
- Price Change (1Y): +15.2%

### Valuation Metrics
- P/E Ratio: 28.5
- Forward P/E: 26.8
- Price-to-Book: 45.2
- PEG Ratio: 1.8

### Financial Health
- Revenue Growth: 5.2% YoY
- Profit Margin: 26.9%
- Operating Margin: 31.6%
- Return on Equity: 17.14%
- Return on Assets: 22.96%

### Growth Trajectory
- Revenue Growth Rate: 0.79%
- Earnings Growth Rate: 9.12%
- Free Cash Flow: $99.6 Billion

## Competitive Landscape

### Key Competitors
1. **Microsoft Corporation (MSFT)**
   - Market Cap: $3.1T
   - Competitive in software and cloud services

2. **Alphabet Inc. (GOOGL)**
   - Market Cap: $1.8T
   - Competes in mobile OS and services

3. **Samsung Electronics**
   - Market Cap: $350B
   - Direct competitor in smartphones

4. **Amazon.com Inc. (AMZN)**
   - Market Cap: $1.6T
   - Competes in services and devices

### Market Position
Apple maintains a strong market position with:
- **Market Share**: 23% in global smartphone market
- **Competitive Advantages**: 
  - Strong brand loyalty
  - Integrated ecosystem
  - Premium positioning
  - Innovation leadership

### Competitive Threats
- Intense competition in smartphone market
- Price sensitivity in emerging markets
- Regulatory challenges
- Supply chain dependencies

## SWOT Analysis

### Strengths
- Strong brand value and customer loyalty
- Integrated ecosystem (hardware, software, services)
- High profit margins
- Strong cash position ($166B)
- Innovation leadership
- Global distribution network

### Weaknesses
- High product prices limit market penetration
- Dependence on iPhone for majority of revenue
- Limited presence in emerging markets
- Supply chain concentration risks

### Opportunities
- Growth in services segment
- Expansion in emerging markets
- New product categories (AR/VR, automotive)
- Healthcare and enterprise solutions
- Subscription services growth

### Threats
- Intense competition from Android manufacturers
- Economic downturns affecting consumer spending
- Regulatory changes and antitrust concerns
- Currency fluctuations
- Supply chain disruptions

## Key Takeaways

1. **Strong Financial Performance**: Apple demonstrates consistent revenue growth and high profitability with strong cash generation.

2. **Market Leadership**: The company maintains a dominant position in premium smartphone market with strong brand value.

3. **Ecosystem Advantage**: Integrated hardware-software-services ecosystem creates customer lock-in and recurring revenue.

4. **Innovation Focus**: Continuous product innovation and R&D investment drive competitive advantage.

5. **Services Growth**: Services segment provides diversification and higher margins, reducing dependence on hardware.

## Risk Factors

### Market Risks
- Economic recession could reduce consumer spending on premium products
- Intense competition in smartphone market
- Market saturation in developed regions

### Operational Risks
- Supply chain disruptions (especially in China)
- Product launch delays or failures
- Key personnel dependencies

### Regulatory Risks
- Antitrust investigations and regulations
- Data privacy regulations
- Trade tensions and tariffs

### Financial Risks
- Currency exchange rate fluctuations
- Interest rate changes affecting cash management
- Credit and counterparty risks

---

**Report Generated**: {timestamp}
**Analysis Type**: Full Analysis
**Period**: 1 Year
"""

    ticker = "AAPL"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Format the report with timestamp
    formatted_report = sample_report.format(timestamp=timestamp)
    
    print(f"\n📝 Sample Report Generated ({len(formatted_report)} characters)")
    print(f"   Ticker: {ticker}")
    print(f"   Timestamp: {timestamp}")
    
    # Generate PDF
    print("\n🔄 Generating PDF...")
    try:
        pdf_data = markdown_to_pdf(formatted_report, ticker, timestamp)
        
        # Check if PDF is valid
        if pdf_data and len(pdf_data) > 0:
            # Check if it starts with PDF magic bytes
            if pdf_data.startswith(b'%PDF'):
                print("✅ PDF generated successfully!")
                print(f"   File size: {len(pdf_data):,} bytes")
                
                # Save to file for testing
                output_file = f"test_report_{ticker}_{timestamp.replace(':', '-').replace(' ', '_')}.pdf"
                with open(output_file, 'wb') as f:
                    f.write(pdf_data)
                
                print(f"\n💾 PDF saved to: {output_file}")
                print(f"   You can now open this file to verify it works correctly!")
                print(f"\n✅ PDF Generation Test: PASSED")
                return True
            else:
                print("❌ PDF generation failed - file doesn't start with PDF magic bytes")
                print(f"   First 100 bytes: {pdf_data[:100]}")
                print("\n⚠️  The generated file is not a valid PDF.")
                return False
        else:
            print("❌ PDF generation failed - empty or no data")
            return False
            
    except Exception as e:
        print(f"❌ PDF generation error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "🚀 " * 20)
    print("QUICK PDF GENERATION TEST")
    print("🚀 " * 20 + "\n")
    print("This test generates a sample report and PDF without running full analysis.")
    print("Saves you 20-25 minutes of waiting time!\n")
    
    success = test_pdf_generation()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ TEST COMPLETE - PDF file generated successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Open the generated PDF file")
        print("2. Verify it opens correctly in your PDF viewer")
        print("3. Check formatting (headings, paragraphs, etc.)")
    else:
        print("\n" + "=" * 60)
        print("❌ TEST FAILED - Check error messages above")
        print("=" * 60)
    
    sys.exit(0 if success else 1)

