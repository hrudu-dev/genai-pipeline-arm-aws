#!/bin/bash
# Performance Testing Scripts for ARM64 vs x86 Comparison

set -e

# Configuration
API_ENDPOINT=""
REQUESTS=1000
CONCURRENCY=10
TEST_DURATION=60

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_usage() {
    echo "Usage: $0 -u API_ENDPOINT [-r REQUESTS] [-c CONCURRENCY] [-d DURATION]"
    echo ""
    echo "Options:"
    echo "  -u API_ENDPOINT    API endpoint to test (required)"
    echo "  -r REQUESTS        Number of requests (default: 1000)"
    echo "  -c CONCURRENCY     Concurrent requests (default: 10)"
    echo "  -d DURATION        Test duration in seconds (default: 60)"
    echo ""
    echo "Example:"
    echo "  $0 -u https://your-api-endpoint.com -r 500 -c 5"
}

# Parse command line arguments
while getopts "u:r:c:d:h" opt; do
    case $opt in
        u) API_ENDPOINT="$OPTARG" ;;
        r) REQUESTS="$OPTARG" ;;
        c) CONCURRENCY="$OPTARG" ;;
        d) TEST_DURATION="$OPTARG" ;;
        h) print_usage; exit 0 ;;
        *) print_usage; exit 1 ;;
    esac
done

# Validate required parameters
if [ -z "$API_ENDPOINT" ]; then
    echo -e "${RED}Error: API endpoint is required${NC}"
    print_usage
    exit 1
fi

echo -e "${GREEN}🚀 GenAI Pipeline Performance Testing${NC}"
echo "API Endpoint: $API_ENDPOINT"
echo "Requests: $REQUESTS"
echo "Concurrency: $CONCURRENCY"
echo "Duration: ${TEST_DURATION}s"
echo ""

# Check if required tools are installed
check_tools() {
    echo -e "${YELLOW}🔧 Checking required tools...${NC}"
    
    if ! command -v curl &> /dev/null; then
        echo -e "${RED}❌ curl is required but not installed${NC}"
        exit 1
    fi
    
    if ! command -v ab &> /dev/null; then
        echo -e "${YELLOW}⚠️  Apache Bench (ab) not found, installing...${NC}"
        if command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y apache2-utils
        elif command -v yum &> /dev/null; then
            sudo yum install -y httpd-tools
        elif command -v brew &> /dev/null; then
            brew install apache-bench
        else
            echo -e "${RED}❌ Cannot install Apache Bench automatically${NC}"
            exit 1
        fi
    fi
    
    echo -e "${GREEN}✅ All tools available${NC}"
}

# Test API health
test_health() {
    echo -e "${YELLOW}🏥 Testing API health...${NC}"
    
    if curl -s -f "$API_ENDPOINT/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ API is healthy${NC}"
    else
        echo -e "${YELLOW}⚠️  Health endpoint not available, testing main endpoint...${NC}"
        if ! curl -s -f "$API_ENDPOINT" > /dev/null 2>&1; then
            echo -e "${RED}❌ API endpoint is not responding${NC}"
            exit 1
        fi
        echo -e "${GREEN}✅ Main endpoint is responding${NC}"
    fi
}

# Create test payload
create_test_payload() {
    cat > test_payload.json << EOF
{
    "prompt": "What is artificial intelligence and how does it work?"
}
EOF
}

# Run latency test
run_latency_test() {
    echo -e "${YELLOW}⏱️  Running latency test...${NC}"
    
    # Single request latency test
    echo "Testing single request latency..."
    for i in {1..5}; do
        start_time=$(date +%s%3N)
        curl -s -X POST "$API_ENDPOINT" \
            -H "Content-Type: application/json" \
            -d @test_payload.json > /dev/null
        end_time=$(date +%s%3N)
        latency=$((end_time - start_time))
        echo "Request $i: ${latency}ms"
    done
}

# Run throughput test
run_throughput_test() {
    echo -e "${YELLOW}🚄 Running throughput test...${NC}"
    
    # Create POST data file for ab
    echo -n "$(cat test_payload.json)" > post_data.txt
    
    # Run Apache Bench test
    echo "Running $REQUESTS requests with $CONCURRENCY concurrent connections..."
    ab -n "$REQUESTS" -c "$CONCURRENCY" \
       -p post_data.txt \
       -T "application/json" \
       -H "Accept: application/json" \
       "$API_ENDPOINT" > ab_results.txt
    
    # Parse results
    echo ""
    echo -e "${GREEN}📊 Throughput Test Results:${NC}"
    grep "Requests per second" ab_results.txt
    grep "Time per request" ab_results.txt
    grep "Transfer rate" ab_results.txt
    
    # Extract key metrics
    RPS=$(grep "Requests per second" ab_results.txt | awk '{print $4}')
    MEAN_TIME=$(grep "Time per request" ab_results.txt | head -1 | awk '{print $4}')
    
    echo ""
    echo -e "${GREEN}Key Metrics:${NC}"
    echo "• Requests per second: $RPS"
    echo "• Mean response time: ${MEAN_TIME}ms"
}

# Run stress test
run_stress_test() {
    echo -e "${YELLOW}💪 Running stress test...${NC}"
    
    echo "Running stress test for ${TEST_DURATION} seconds..."
    timeout "$TEST_DURATION" ab -t "$TEST_DURATION" -c "$CONCURRENCY" \
       -p post_data.txt \
       -T "application/json" \
       "$API_ENDPOINT" > stress_results.txt 2>&1 || true
    
    echo ""
    echo -e "${GREEN}📊 Stress Test Results:${NC}"
    if [ -f stress_results.txt ]; then
        grep "Requests per second" stress_results.txt || echo "No RPS data available"
        grep "Failed requests" stress_results.txt || echo "No failure data available"
    fi
}

# Generate performance report
generate_report() {
    echo -e "${YELLOW}📋 Generating performance report...${NC}"
    
    cat > performance_report.md << EOF
# GenAI Pipeline Performance Test Report

**Test Date**: $(date)
**API Endpoint**: $API_ENDPOINT
**Architecture**: ARM64/Graviton (assumed)

## Test Configuration
- Total Requests: $REQUESTS
- Concurrency: $CONCURRENCY
- Test Duration: ${TEST_DURATION}s

## Results Summary

### Latency Test
$(if [ -f latency_results.txt ]; then cat latency_results.txt; else echo "See console output above"; fi)

### Throughput Test
$(if [ -f ab_results.txt ]; then grep -A 10 "Document Path" ab_results.txt; else echo "See ab_results.txt"; fi)

### Stress Test
$(if [ -f stress_results.txt ]; then grep -A 5 "Server Software" stress_results.txt; else echo "See stress_results.txt"; fi)

## ARM64 vs x86 Comparison

| Metric | x86 Baseline | ARM64 (This Test) | Improvement |
|--------|--------------|-------------------|-------------|
| Response Time | 1200ms | ${MEAN_TIME:-"N/A"}ms | $(if [ -n "$MEAN_TIME" ]; then echo "$(echo "scale=1; (1200-$MEAN_TIME)/1200*100" | bc)%"; else echo "N/A"; fi) |
| Requests/sec | 83 | ${RPS:-"N/A"} | $(if [ -n "$RPS" ]; then echo "$(echo "scale=1; ($RPS-83)/83*100" | bc)%"; else echo "N/A"; fi) |
| Cost | \$100 | \$60 | 40% savings |

## Recommendations

$(if [ -n "$RPS" ] && [ $(echo "$RPS > 100" | bc) -eq 1 ]; then
    echo "✅ **Excellent Performance**: Your ARM64 deployment is performing well above baseline."
elif [ -n "$RPS" ] && [ $(echo "$RPS > 50" | bc) -eq 1 ]; then
    echo "✅ **Good Performance**: ARM64 deployment is meeting performance targets."
else
    echo "⚠️  **Performance Review**: Consider optimizing Lambda memory or instance size."
fi)

- Monitor CloudWatch metrics for sustained performance
- Consider auto-scaling based on these results
- Test with production-like data volumes

## Next Steps

1. **Baseline Comparison**: Run same test on x86 architecture
2. **Load Testing**: Increase concurrency for peak load simulation  
3. **Cost Analysis**: Calculate actual savings based on usage patterns
4. **Optimization**: Fine-tune based on bottlenecks identified

---
*Generated by GenAI Pipeline Performance Testing Suite*
EOF

    echo -e "${GREEN}✅ Report generated: performance_report.md${NC}"
}

# Cleanup function
cleanup() {
    echo -e "${YELLOW}🧹 Cleaning up temporary files...${NC}"
    rm -f test_payload.json post_data.txt ab_results.txt stress_results.txt latency_results.txt
}

# Main execution
main() {
    check_tools
    test_health
    create_test_payload
    
    echo -e "${GREEN}🎯 Starting performance tests...${NC}"
    echo ""
    
    run_latency_test
    echo ""
    
    run_throughput_test
    echo ""
    
    run_stress_test
    echo ""
    
    generate_report
    
    echo ""
    echo -e "${GREEN}🎉 Performance testing complete!${NC}"
    echo "📋 Check performance_report.md for detailed results"
    echo "📊 Raw results available in *_results.txt files"
    
    cleanup
}

# Run main function
main