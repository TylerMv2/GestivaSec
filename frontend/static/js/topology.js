// Gestiva Observability Topology Render Engine - Windows 11 Soft Cyberpunk Style

let observerInitialized = false;

async function initTopology() {
    const canvas = document.getElementById('topology-canvas');
    canvas.innerHTML = '<div class="mono" style="color:var(--neon-purple); padding: 50px; text-align:center;"><i class="fa-solid fa-spinner fa-spin"></i> GENERANDO TOPOLOGÍA DE RED...</div>';
    
    try {
        const data = await API.getTopology();
        window.lastTopologyData = data;
        renderSVG(data);
        
        if (!observerInitialized) {
            let resizeTimeout;
            const resizeObserver = new ResizeObserver(entries => {
                clearTimeout(resizeTimeout);
                resizeTimeout = setTimeout(() => {
                    if (window.lastTopologyData) {
                        renderSVG(window.lastTopologyData);
                    }
                }, 100);
            });
            const card = document.getElementById('topology-card');
            if (card) {
                resizeObserver.observe(card);
            }
            observerInitialized = true;
        }
    } catch (e) {
        canvas.innerHTML = `<div class="mono" style="color:var(--neon-magenta); padding:50px; text-align:center;"><i class="fa-solid fa-triangle-exclamation"></i> ERROR AL CARGAR TOPOLOGÍA: ${e.message}</div>`;
    }
}

function renderSVG(data) {
    const canvas = document.getElementById('topology-canvas');
    canvas.innerHTML = '';
    
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    
    // Create SVG element
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("width", "100%");
    svg.setAttribute("height", "100%");
    svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
    svg.style.background = "transparent";
    
    // SVG glow filters (softer glows)
    const defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
    defs.innerHTML = `
        <filter id="fluent-glow-purple" x="-30%" y="-30%" width="160%" height="160%">
            <feGaussianBlur stdDeviation="8" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
        <filter id="fluent-glow-green" x="-30%" y="-30%" width="160%" height="160%">
            <feGaussianBlur stdDeviation="8" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
        <filter id="fluent-glow-magenta" x="-30%" y="-30%" width="160%" height="160%">
            <feGaussianBlur stdDeviation="8" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
    `;
    svg.appendChild(defs);
    
    // 1. Calculate expanded grid layout coordinates
    const nodeCoords = {
        "internet": { x: width * 0.08, y: height * 0.5 },
        "firewall": { x: width * 0.24, y: height * 0.5 },
        "switch": { x: width * 0.44, y: height * 0.5 }
    };
    
    // Filter hosts (servers, switch, VMs)
    const hosts = data.nodes.filter(n => n.id.startsWith("host_"));
    
    hosts.forEach((host, idx) => {
        // Broad vertical distribution across 75% of height
        const verticalFactor = hosts.length > 1 ? idx / (hosts.length - 1) : 0.5;
        const yCoord = height * 0.15 + (verticalFactor * height * 0.7);
        
        nodeCoords[host.id] = {
            x: width * 0.68, // Expanded horizontally
            y: yCoord
        };
        
        // Filter services belonging to this host
        const svcs = data.nodes.filter(n => 
            n.id.startsWith("svc_") && 
            data.links.some(l => l.source === host.id && l.target === n.id)
        );
        
        // Spread services vertically centered relative to their parent host
        svcs.forEach((svc, sIdx) => {
            const verticalOffset = svcs.length > 1 ? (sIdx - (svcs.length - 1) / 2) * 60 : 0;
            nodeCoords[svc.id] = {
                x: width * 0.88, // Pushed to the right edge
                y: yCoord + verticalOffset
            };
        });
    });
    
    // Ensure fallback positions
    data.nodes.forEach(n => {
        if (!nodeCoords[n.id]) {
            nodeCoords[n.id] = { x: width / 2, y: height / 2 };
        }
    });
    
    // 2. Draw link paths with soft dashes
    data.links.forEach(link => {
        const sourceCoord = nodeCoords[link.source];
        const targetCoord = nodeCoords[link.target];
        
        if (sourceCoord && targetCoord) {
            const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
            line.setAttribute("x1", sourceCoord.x);
            line.setAttribute("y1", sourceCoord.y);
            line.setAttribute("x2", targetCoord.x);
            line.setAttribute("y2", targetCoord.y);
            
            // Softer grid lines
            line.setAttribute("stroke", "rgba(199, 125, 255, 0.12)");
            line.setAttribute("stroke-width", "2");
            line.setAttribute("stroke-dasharray", "6,6");
            
            // Soft data packet transmission animation
            const animate = document.createElementNS("http://www.w3.org/2000/svg", "animate");
            animate.setAttribute("attributeName", "stroke-dashoffset");
            animate.setAttribute("values", "120;0");
            animate.setAttribute("dur", "6s");
            animate.setAttribute("repeatCount", "indefinite");
            line.appendChild(animate);
            
            svg.appendChild(line);
        }
    });
    
    // 3. Draw nodes as Fluent circular shapes
    data.nodes.forEach(node => {
        const coord = nodeCoords[node.id];
        if (!coord) return;
        
        const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
        g.style.cursor = "pointer";
        g.addEventListener("click", () => showNodeDetails(node));
        
        // Define clean Windows 11 style variables
        let radius = 22;
        let strokeColor = "rgba(255, 255, 255, 0.15)";
        let fillColor = "rgba(26, 17, 48, 0.85)";
        let glowFilter = "";
        let iconHtml = "";
        
        // Determine type-specific icons and colors
        if (node.status === "DOWN") {
            strokeColor = "var(--neon-magenta)";
            fillColor = "rgba(255, 84, 176, 0.08)";
            glowFilter = "url(#fluent-glow-magenta)";
            iconHtml = "&#xf057;"; // FontAwesome cross circle
        } else {
            // UP Status
            if (node.type === "Firewall") {
                strokeColor = "var(--neon-orange)";
                fillColor = "rgba(255, 158, 0, 0.08)";
                iconHtml = "&#xf505;"; // Shield
            } else if (node.id === "internet") {
                strokeColor = "var(--neon-blue)";
                fillColor = "rgba(58, 134, 255, 0.08)";
                iconHtml = "&#xf0ac;"; // Globe
            } else if (node.id === "switch") {
                strokeColor = "var(--neon-purple)";
                fillColor = "rgba(199, 125, 255, 0.08)";
                iconHtml = "&#xf6ff;"; // Server stack
            } else if (node.type === "Service") {
                // Smaller service node
                radius = 16;
                strokeColor = "var(--text-muted)";
                fillColor = "rgba(255, 255, 255, 0.03)";
                iconHtml = "&#xf120;"; // Code/Terminal
            } else {
                // Server / Client UP
                strokeColor = "var(--neon-green)";
                fillColor = "rgba(6, 214, 160, 0.08)";
                glowFilter = "url(#fluent-glow-green)";
                iconHtml = "&#xf233;"; // Server
            }
        }
        
        // Outer pulsing ring for DOWN nodes
        if (node.status === "DOWN") {
            const pulse = document.createElementNS("http://www.w3.org/2000/svg", "circle");
            pulse.setAttribute("cx", coord.x);
            pulse.setAttribute("cy", coord.y);
            pulse.setAttribute("r", radius);
            pulse.setAttribute("fill", "none");
            pulse.setAttribute("stroke", strokeColor);
            pulse.setAttribute("stroke-width", "1.5");
            pulse.setAttribute("opacity", "0.7");
            
            const animR = document.createElementNS("http://www.w3.org/2000/svg", "animate");
            animR.setAttribute("attributeName", "r");
            animR.setAttribute("values", `${radius};${radius + 18}`);
            animR.setAttribute("dur", "2s");
            animR.setAttribute("repeatCount", "indefinite");
            
            const animO = document.createElementNS("http://www.w3.org/2000/svg", "animate");
            animO.setAttribute("attributeName", "opacity");
            animO.setAttribute("values", "0.7;0");
            animO.setAttribute("dur", "2s");
            animO.setAttribute("repeatCount", "indefinite");
            
            pulse.appendChild(animR);
            pulse.appendChild(animO);
            g.appendChild(pulse);
        }
        
        // Base Circle Capsule
        const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        circle.setAttribute("cx", coord.x);
        circle.setAttribute("cy", coord.y);
        circle.setAttribute("r", radius);
        circle.setAttribute("fill", fillColor);
        circle.setAttribute("stroke", strokeColor);
        circle.setAttribute("stroke-width", "2");
        if (glowFilter) {
            circle.setAttribute("filter", glowFilter);
        }
        g.appendChild(circle);
        
        // Render FontAwesome icon inside the node circle
        const iconText = document.createElementNS("http://www.w3.org/2000/svg", "text");
        iconText.setAttribute("x", coord.x);
        iconText.setAttribute("y", coord.y + 5);
        iconText.setAttribute("text-anchor", "middle");
        iconText.setAttribute("fill", strokeColor);
        iconText.setAttribute("font-family", '"Font Awesome 6 Free"');
        iconText.setAttribute("font-weight", "900");
        iconText.setAttribute("font-size", radius > 16 ? "15px" : "11px");
        iconText.innerHTML = iconHtml;
        g.appendChild(iconText);
        
        // Node labels
        const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
        text.setAttribute("x", coord.x);
        text.setAttribute("y", coord.y + radius + 16);
        text.setAttribute("text-anchor", "middle");
        text.setAttribute("fill", "var(--text-primary)");
        text.setAttribute("font-family", "Outfit");
        text.setAttribute("font-weight", "500");
        text.setAttribute("font-size", "11px");
        
        const lines = node.label.split("\n");
        lines.forEach((line, lineIdx) => {
            const tspan = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
            tspan.setAttribute("x", coord.x);
            tspan.setAttribute("dy", lineIdx === 0 ? 0 : 12);
            tspan.textContent = line;
            text.appendChild(tspan);
        });
        
        g.appendChild(text);
        svg.appendChild(g);
    });
    
    canvas.appendChild(svg);
}

function showNodeDetails(node) {
    const panel = document.getElementById('node-detail-panel');
    
    let html = `
        <div style="border: 1px solid var(--border-soft); background:rgba(255, 255, 255, 0.02); padding:15px; border-radius:12px;">
            <div style="font-family:var(--font-main); font-size:1.05rem; font-weight:600; color:var(--neon-purple); border-bottom:1px solid rgba(255,255,255,0.05); padding-bottom:6px; margin-bottom:10px;">
                ${node.label.split('\n')[0]}
            </div>
            <table style="width:100%; border-collapse:collapse; font-size:0.85rem;" class="mono">
                <tr>
                    <td style="padding:5px 0; color:var(--text-muted);">TIPO:</td>
                    <td style="padding:5px 0; font-weight:600; text-align:right;">${node.type}</td>
                </tr>
                <tr>
                    <td style="padding:5px 0; color:var(--text-muted);">ESTADO:</td>
                    <td style="padding:5px 0; text-align:right;">
                        <span class="cyber-badge ${node.status === 'UP' ? 'green' : 'magenta'}">${node.status}</span>
                    </td>
                </tr>
    `;
    
    if (node.latency !== undefined) {
        html += `
            <tr>
                <td style="padding:5px 0; color:var(--text-muted);">LATENCIA:</td>
                <td style="padding:5px 0; font-weight:600; text-align:right; color:var(--neon-purple);">${node.latency.toFixed(2)} ms</td>
            </tr>
        `;
    }
    
    html += `
            </table>
        </div>
    `;
    
    panel.innerHTML = html;
}
