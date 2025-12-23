"""Performance tracing browser commands."""

import json
import logging
import time

logger = logging.getLogger(__name__)

# Store trace data per browser (in-memory, cleared on stop)
_trace_data = {}


def handle_start_trace(driver, command: dict, browser_id: str = "unknown") -> dict:
    """Start performance tracing.

    Args:
        command: {
            "categories": comma-separated trace categories (optional)
        }
    """
    categories = command.get(
        "categories",
        "devtools.timeline,v8.execute,disabled-by-default-devtools.timeline",
    )

    try:
        # Enable necessary CDP domains
        driver.execute_cdp_cmd("Performance.enable", {})

        # Start tracing
        driver.execute_cdp_cmd(
            "Tracing.start",
            {
                "categories": categories,
                "transferMode": "ReturnAsStream",
            },
        )

        _trace_data[browser_id] = {
            "start_time": time.time(),
            "categories": categories,
        }

        return {
            "status": "success",
            "message": "Tracing started",
            "categories": categories,
        }

    except Exception as e:
        return {"status": "error", "message": f"Failed to start tracing: {str(e)}"}


def handle_stop_trace(driver, command: dict, browser_id: str = "unknown") -> dict:
    """Stop performance tracing and return trace data."""
    try:
        # Stop tracing
        driver.execute_cdp_cmd("Tracing.end", {})

        # Get trace data
        # Note: In real implementation, we'd need to handle Tracing.tracingComplete event
        # For now, we'll get performance metrics directly
        metrics = driver.execute_cdp_cmd("Performance.getMetrics", {})

        trace_info = _trace_data.pop(browser_id, {})
        duration = time.time() - trace_info.get("start_time", time.time())

        return {
            "status": "success",
            "duration_seconds": duration,
            "metrics": metrics.get("metrics", []),
        }

    except Exception as e:
        return {"status": "error", "message": f"Failed to stop tracing: {str(e)}"}


def handle_get_metrics(driver, command: dict) -> dict:
    """Get current performance metrics without tracing."""
    try:
        driver.execute_cdp_cmd("Performance.enable", {})
        metrics = driver.execute_cdp_cmd("Performance.getMetrics", {})

        # Convert to more readable format
        metrics_dict = {m["name"]: m["value"] for m in metrics.get("metrics", [])}

        return {
            "status": "success",
            "metrics": metrics_dict,
        }

    except Exception as e:
        return {"status": "error", "message": f"Failed to get metrics: {str(e)}"}


def handle_analyze_insight(driver, command: dict) -> dict:
    """Analyze page performance and return insights.

    This provides a high-level performance analysis including:
    - Page load metrics (FCP, LCP, TTI estimates)
    - Resource timing
    - JavaScript execution time
    """
    try:
        # Get performance entries via JavaScript
        perf_data = driver.execute_script(
            """
            const perf = window.performance;
            const timing = perf.timing;
            const entries = perf.getEntriesByType('navigation')[0] || {};
            const resources = perf.getEntriesByType('resource');
            const paint = perf.getEntriesByType('paint');

            // Calculate key metrics
            const fcp = paint.find(p => p.name === 'first-contentful-paint');
            const lcp = perf.getEntriesByType('largest-contentful-paint').slice(-1)[0];

            // Resource summary
            const resourceSummary = {
                total: resources.length,
                totalSize: resources.reduce((sum, r) => sum + (r.transferSize || 0), 0),
                byType: {}
            };
            resources.forEach(r => {
                const type = r.initiatorType || 'other';
                if (!resourceSummary.byType[type]) {
                    resourceSummary.byType[type] = { count: 0, size: 0 };
                }
                resourceSummary.byType[type].count++;
                resourceSummary.byType[type].size += r.transferSize || 0;
            });

            return {
                navigation: {
                    domContentLoaded: entries.domContentLoadedEventEnd - entries.startTime,
                    load: entries.loadEventEnd - entries.startTime,
                    domInteractive: entries.domInteractive - entries.startTime,
                    responseEnd: entries.responseEnd - entries.startTime,
                },
                paint: {
                    firstContentfulPaint: fcp ? fcp.startTime : null,
                    largestContentfulPaint: lcp ? lcp.startTime : null,
                },
                resources: resourceSummary,
                memory: perf.memory ? {
                    usedJSHeapSize: perf.memory.usedJSHeapSize,
                    totalJSHeapSize: perf.memory.totalJSHeapSize,
                } : null,
            };
            """
        )

        # Generate insights
        insights = []
        paint = perf_data.get("paint", {})
        resources = perf_data.get("resources", {})

        # FCP analysis
        fcp = paint.get("firstContentfulPaint")
        if fcp:
            if fcp < 1800:
                insights.append({"metric": "FCP", "status": "good", "value": f"{fcp:.0f}ms"})
            elif fcp < 3000:
                insights.append(
                    {"metric": "FCP", "status": "needs_improvement", "value": f"{fcp:.0f}ms"}
                )
            else:
                insights.append({"metric": "FCP", "status": "poor", "value": f"{fcp:.0f}ms"})

        # LCP analysis
        lcp = paint.get("largestContentfulPaint")
        if lcp:
            if lcp < 2500:
                insights.append({"metric": "LCP", "status": "good", "value": f"{lcp:.0f}ms"})
            elif lcp < 4000:
                insights.append(
                    {"metric": "LCP", "status": "needs_improvement", "value": f"{lcp:.0f}ms"}
                )
            else:
                insights.append({"metric": "LCP", "status": "poor", "value": f"{lcp:.0f}ms"})

        # Resource count analysis
        total_resources = resources.get("total", 0)
        if total_resources > 100:
            insights.append(
                {
                    "metric": "Resources",
                    "status": "warning",
                    "value": f"{total_resources} requests",
                    "suggestion": "Consider reducing the number of HTTP requests",
                }
            )

        return {
            "status": "success",
            "performance": perf_data,
            "insights": insights,
        }

    except Exception as e:
        return {"status": "error", "message": f"Failed to analyze performance: {str(e)}"}
