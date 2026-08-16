"""Exercise the optional vegetation module in a real headless Chromium page."""

from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
URL = "http://127.0.0.1:8946/validation/vegetation-runtime-harness.html"
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")


def main() -> None:
    console_errors: list[str] = []
    request_failures: list[str] = []
    bad_responses: list[dict[str, object]] = []
    mobile_glb_requests: list[str] = []
    mobile_console_errors: list[str] = []
    constrained_glb_requests: list[str] = []
    constrained_console_errors: list[str] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True,
            executable_path=str(CHROME),
            args=["--use-angle=swiftshader", "--enable-webgl"],
        )
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.on(
            "console",
            lambda message: console_errors.append(message.text)
            if message.type == "error"
            else None,
        )
        page.on("requestfailed", lambda request: request_failures.append(request.url))
        page.on(
            "response",
            lambda response: bad_responses.append({"status": response.status, "url": response.url})
            if response.status >= 400
            else None,
        )
        page.goto(URL, wait_until="networkidle", timeout=60_000)
        page.wait_for_function("window.__done === true", timeout=60_000)
        audit = page.evaluate("window.__audit")
        state = page.evaluate(
            """() => ({
              datasetStatus: document.documentElement.dataset.viewerVegetation,
              datasetTriangles: document.documentElement.dataset.viewerVegetationTriangles,
              datasetDrawCalls: document.documentElement.dataset.viewerVegetationDrawCalls,
              enhancedGroup: Boolean(window.__liveVegetationAudit),
              webgl2: Boolean(document.querySelector('canvas').getContext('webgl2'))
            })"""
        )
        page.screenshot(path=str(ROOT / "validation" / "vegetation-runtime-harness.png"))

        mobile_page = browser.new_page(
            viewport={"width": 390, "height": 844},
            is_mobile=True,
            has_touch=True,
        )
        mobile_page.on(
            "request",
            lambda request: mobile_glb_requests.append(request.url)
            if request.url.lower().endswith(".glb") or ".glb?" in request.url.lower()
            else None,
        )
        mobile_page.on(
            "console",
            lambda message: mobile_console_errors.append(message.text)
            if message.type == "error"
            else None,
        )
        mobile_page.goto(URL + "?mobile=1", wait_until="networkidle", timeout=60_000)
        mobile_page.wait_for_function("window.__done === true", timeout=60_000)
        mobile_audit = mobile_page.evaluate("window.__audit")

        constrained_page = browser.new_page(
            viewport={"width": 390, "height": 844},
            is_mobile=True,
            has_touch=True,
        )
        constrained_page.on(
            "request",
            lambda request: constrained_glb_requests.append(request.url)
            if request.url.lower().endswith(".glb") or ".glb?" in request.url.lower()
            else None,
        )
        constrained_page.on(
            "console",
            lambda message: constrained_console_errors.append(message.text)
            if message.type == "error"
            else None,
        )
        constrained_page.goto(URL + "?mobile=1&constrained=1", wait_until="networkidle", timeout=60_000)
        constrained_page.wait_for_function("window.__done === true", timeout=60_000)
        constrained_audit = constrained_page.evaluate("window.__audit")
        browser.close()

    expected = {
        "status": "enhanced",
        "treeInstances": 4,
        "hedgeInstances": 18,
        "hedgeCloneInstances": 108,
        "displayedTriangles": 1_082_996,
        "drawCalls": 120,
        "originalsHidden": 38,
    }
    checks = {
        key: audit.get(key) == value
        for key, value in expected.items()
    }
    checks.update(
        {
            "assets_loaded": audit["assets"]["tree"]["loaded"] and audit["assets"]["hedge"]["loaded"],
            "dataset_status": state["datasetStatus"] == "enhanced",
            "dataset_triangles": state["datasetTriangles"] == "1082996",
            "dataset_draw_calls": state["datasetDrawCalls"] == "120",
            "webgl2": state["webgl2"],
            "console_errors_zero": not console_errors,
            "request_failures_zero": not request_failures,
            "http_bad_zero": not bad_responses,
            "mobile_status": mobile_audit["status"] == "enhanced" and mobile_audit["mode"] == "enhanced-mobile",
            "mobile_instances": mobile_audit["treeInstances"] == 4 and mobile_audit["hedgeInstances"] == 18 and mobile_audit["hedgeCloneInstances"] == 108,
            "mobile_triangles": mobile_audit["displayedTriangles"] == 1_082_996 and mobile_audit["drawCalls"] == 120,
            "mobile_optional_glb_requests": len(mobile_glb_requests) == 2,
            "mobile_console_errors_zero": not mobile_console_errors,
            "constrained_status": constrained_audit["status"] == "mobile-fallback",
            "constrained_instances_zero": constrained_audit["treeInstances"] == 0 and constrained_audit["hedgeInstances"] == 0 and constrained_audit["hedgeCloneInstances"] == 0,
            "constrained_triangles_zero": constrained_audit["displayedTriangles"] == 0 and constrained_audit["drawCalls"] == 0,
            "constrained_optional_glb_requests_zero": not constrained_glb_requests,
            "constrained_console_errors_zero": not constrained_console_errors,
        }
    )
    result = "PASS" if all(checks.values()) else "FAIL"
    report = {
        "result": result,
        "url": URL,
        "viewport": "1440x900",
        "audit": audit,
        "state": state,
        "mobileAudit": mobile_audit,
        "mobileGlbRequests": mobile_glb_requests,
        "mobileConsoleErrors": mobile_console_errors,
        "constrainedAudit": constrained_audit,
        "constrainedGlbRequests": constrained_glb_requests,
        "constrainedConsoleErrors": constrained_console_errors,
        "consoleErrors": console_errors,
        "requestFailures": request_failures,
        "badResponses": bad_responses,
        "checks": checks,
    }
    (ROOT / "validation" / "vegetation-runtime-validation.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"VEGETATION_BROWSER_RUNTIME={result} "
        f"trees={audit.get('treeInstances')} hedge_segments={audit.get('hedgeInstances')} "
        f"hedge_clones={audit.get('hedgeCloneInstances')} "
        f"displayed_triangles={audit.get('displayedTriangles')} draw_calls={audit.get('drawCalls')} "
        f"load_ms={audit.get('loadMs')} webgl2={state['webgl2']} "
        f"console_errors={len(console_errors)} request_failures={len(request_failures)} "
        f"http_bad={len(bad_responses)} mobile={mobile_audit.get('status')} "
        f"mobile_glb_requests={len(mobile_glb_requests)} constrained={constrained_audit.get('status')} "
        f"constrained_glb_requests={len(constrained_glb_requests)}"
    )
    if result != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
