const canvas = document.querySelector('#hero-canvas');
const portrait = document.querySelector('.portrait-photo');

portrait?.addEventListener('error', () => portrait.classList.add('is-missing'));
if (portrait?.complete && !portrait.naturalWidth) portrait.classList.add('is-missing');

const feedbackForm = document.querySelector('#feedback-form');
feedbackForm?.addEventListener('submit', (event) => {
  event.preventDefault();
  const values = new FormData(feedbackForm);
  const subject = `Portfolio feedback from ${values.get('name')}`;
  const body = `Name: ${values.get('name')}\nEmail: ${values.get('email')}\n\n${values.get('message')}`;
  const email = feedbackForm.dataset.email;
  document.querySelector('#feedback-status').textContent = 'Opening your email app with the message ready to send.';
  window.location.href = `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
});

const smsForm = document.querySelector('#sms-form');
smsForm?.addEventListener('submit', (event) => {
  event.preventDefault();
  const phone = smsForm.dataset.phone.replace(/[^\d+]/g, '');
  const status = document.querySelector('#sms-status');
  if (!phone) {
    status.textContent = 'Text messaging is not set up yet. Please use the email link instead.';
    return;
  }
  const values = new FormData(smsForm);
  const body = `Hi, I’m ${values.get('name')}. ${values.get('message')}`;
  status.textContent = 'Opening your messaging app with the text ready to send.';
  window.location.href = `sms:${phone}?body=${encodeURIComponent(body)}`;
});

if (canvas) {
  try {
    const THREE = await import('https://cdn.jsdelivr.net/npm/three@0.169.0/build/three.module.js');
    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true, preserveDrawingBuffer: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
    renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.15;

    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0xf4f7f3, 0.012);
    const camera = new THREE.PerspectiveCamera(36, canvas.clientWidth / canvas.clientHeight, 0.1, 100);
    camera.position.set(0.2, 2.1, 8.8);
    camera.lookAt(0, 0, 0);
    scene.add(new THREE.HemisphereLight(0xf4fff6, 0x34473a, 2.3));
    const keyLight = new THREE.DirectionalLight(0xe4ffe9, 4.4);
    keyLight.position.set(-3, 6, 5);
    scene.add(keyLight);
    const tealLight = new THREE.PointLight(0x57d5a0, 24, 12);
    tealLight.position.set(-2.6, 1.5, 3);
    scene.add(tealLight);
    const coralLight = new THREE.PointLight(0xff765d, 20, 11);
    coralLight.position.set(2.8, -0.5, 2);
    scene.add(coralLight);

    const grid = new THREE.GridHelper(18, 32, 0x8da99a, 0xd4dfd7);
    grid.position.y = -1.72;
    grid.material.transparent = true;
    grid.material.opacity = 0.7;
    scene.add(grid);

    const world = new THREE.Group();
    scene.add(world);
    const server = new THREE.Group();
    server.position.set(-0.55, -0.05, 0);
    world.add(server);

    const chassisMaterial = new THREE.MeshPhysicalMaterial({ color: 0x192722, metalness: 0.72, roughness: 0.27, clearcoat: 0.7 });
    const edgeMaterial = new THREE.LineBasicMaterial({ color: 0x6fd4a3, transparent: true, opacity: 0.62 });
    const addPanel = (width, height, depth, x, y, z, material = chassisMaterial) => {
      const mesh = new THREE.Mesh(new THREE.BoxGeometry(width, height, depth), material);
      mesh.position.set(x, y, z);
      server.add(mesh);
      const outline = new THREE.LineSegments(new THREE.EdgesGeometry(mesh.geometry), edgeMaterial);
      outline.position.copy(mesh.position);
      server.add(outline);
      return mesh;
    };

    addPanel(1.65, 2.8, 1.05, 0, 0, 0);
    const shelfMaterial = new THREE.MeshStandardMaterial({ color: 0x28483a, metalness: 0.48, roughness: 0.34 });
    const ledMaterial = new THREE.MeshBasicMaterial({ color: 0x72f0ba });
    const warmLedMaterial = new THREE.MeshBasicMaterial({ color: 0xff795e });
    for (let row = 0; row < 4; row += 1) {
      const y = -0.91 + row * 0.59;
      const shelf = new THREE.Mesh(new THREE.BoxGeometry(1.35, 0.43, 0.12), shelfMaterial);
      shelf.position.set(0, y, 0.57);
      server.add(shelf);
      for (let light = 0; light < 3; light += 1) {
        const dot = new THREE.Mesh(new THREE.SphereGeometry(0.035, 12, 12), light === 0 && row === 2 ? warmLedMaterial : ledMaterial);
        dot.position.set(-0.47 + light * 0.14, y, 0.65);
        server.add(dot);
      }
    }

    const database = new THREE.Group();
    database.position.set(2.05, -0.35, -0.45);
    world.add(database);
    const databaseMaterial = new THREE.MeshPhysicalMaterial({ color: 0x286247, metalness: 0.36, roughness: 0.24, transparent: true, opacity: 0.78, clearcoat: 1 });
    const cylinder = new THREE.Mesh(new THREE.CylinderGeometry(0.78, 0.78, 1.55, 48, 1, false), databaseMaterial);
    database.add(cylinder);
    const cylinderEdges = new THREE.LineSegments(new THREE.EdgesGeometry(cylinder.geometry), new THREE.LineBasicMaterial({ color: 0x8df0bd, transparent: true, opacity: 0.65 }));
    database.add(cylinderEdges);
    const databaseRing = new THREE.Mesh(new THREE.TorusGeometry(0.79, 0.025, 8, 64), new THREE.MeshBasicMaterial({ color: 0x8df0bd }));
    databaseRing.position.y = 0.52;
    database.add(databaseRing);

    const orbit = new THREE.Mesh(
      new THREE.TorusGeometry(2.25, 0.012, 5, 180),
      new THREE.MeshBasicMaterial({ color: 0x61c99a, transparent: true, opacity: 0.5 })
    );
    orbit.rotation.set(1.05, 0.1, -0.25);
    orbit.position.set(0.1, 0.05, -0.15);
    world.add(orbit);
    const secondOrbit = orbit.clone();
    secondOrbit.material = orbit.material.clone();
    secondOrbit.material.color.set(0xe47c66);
    secondOrbit.material.opacity = 0.37;
    secondOrbit.scale.setScalar(1.27);
    secondOrbit.rotation.set(0.78, -0.44, 0.4);
    world.add(secondOrbit);

    const dataMaterial = new THREE.MeshStandardMaterial({ color: 0xf18a6d, emissive: 0x5a1d12, metalness: 0.25, roughness: 0.25 });
    const dataNodes = [];
    for (let index = 0; index < 9; index += 1) {
      const node = new THREE.Mesh(new THREE.SphereGeometry(index % 3 === 0 ? 0.075 : 0.045, 16, 16), dataMaterial);
      node.userData.phase = (index / 9) * Math.PI * 2;
      node.userData.radius = 2.15 + (index % 3) * 0.27;
      world.add(node);
      dataNodes.push(node);
    }

    const floaters = [];
    [[-2.7, 1.2, -0.7, 0.22, 0x377fba], [2.8, 1.4, -1.2, 0.16, 0xe3c244], [1.1, 2.05, 0.2, 0.12, 0x1d6847]].forEach(([x, y, z, size, color]) => {
      const material = new THREE.MeshStandardMaterial({ color, metalness: 0.55, roughness: 0.23, emissive: color, emissiveIntensity: 0.08 });
      const object = new THREE.Mesh(new THREE.IcosahedronGeometry(size, 1), material);
      object.position.set(x, y, z);
      object.userData.offset = y;
      world.add(object);
      floaters.push(object);
    });

    let targetX = 0;
    let targetY = 0;
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const resize = () => {
      const width = canvas.clientWidth;
      const height = canvas.clientHeight;
      if (!width || !height) return;
      renderer.setSize(width, height, false);
      camera.aspect = width / height;
      world.scale.setScalar(width < 600 ? 0.94 : 1);
      camera.position.set(width < 600 ? 0.15 : 0.2, width < 600 ? 2.6 : 2.1, width < 600 ? 9.6 : 8.8);
      camera.lookAt(width < 600 ? 0.35 : 0.1, 0, 0);
      camera.updateProjectionMatrix();
    };
    const observer = new ResizeObserver(resize);
    observer.observe(canvas);
    window.addEventListener('pointermove', (event) => {
      targetY = (event.clientX / window.innerWidth - 0.5) * 0.18;
      targetX = (event.clientY / window.innerHeight - 0.5) * 0.1;
    }, { passive: true });
    const clock = new THREE.Clock();
    const animate = () => {
      const time = clock.getElapsedTime();
      world.rotation.x += (targetX - world.rotation.x) * 0.025;
      world.rotation.y += (targetY + Math.sin(time * 0.22) * 0.08 - world.rotation.y) * 0.025;
      server.rotation.y = Math.sin(time * 0.35) * 0.045;
      database.rotation.y = time * 0.15;
      database.position.y = -0.35 + Math.sin(time * 0.7) * 0.08;
      dataNodes.forEach((node) => {
        const angle = time * 0.23 + node.userData.phase;
        node.position.set(Math.cos(angle) * node.userData.radius, Math.sin(angle * 1.4) * 1.2, Math.sin(angle) * node.userData.radius - 0.15);
      });
      floaters.forEach((object, index) => {
        object.rotation.x = time * (0.16 + index * 0.04);
        object.rotation.y = -time * (0.19 + index * 0.03);
        object.position.y = object.userData.offset + Math.sin(time * 0.8 + index) * 0.12;
      });
      renderer.render(scene, camera);
      requestAnimationFrame(animate);
    };
    resize();
    if (reducedMotion) renderer.render(scene, camera);
    else animate();
  } catch (error) {
    canvas.dataset.scene = 'unavailable';
  }
}

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });
document.querySelectorAll('.project-row, .section-heading, .experience-section, .about-section, .contact-section').forEach((element) => {
  element.classList.add('reveal');
  revealObserver.observe(element);
});

const launcher = document.querySelector('#chat-launcher');
const panel = document.querySelector('#chat-panel');
const closeButton = document.querySelector('#chat-close');
const form = document.querySelector('#chat-form');
const input = document.querySelector('#chat-input');
const messages = document.querySelector('#chat-messages');
const modeLabel = document.querySelector('#chat-mode');

function setChatOpen(open) {
  panel.classList.toggle('is-open', open);
  panel.setAttribute('aria-hidden', String(!open));
  launcher.setAttribute('aria-expanded', String(open));
  if (open) input.focus();
}

function addMessage(text, role) {
  const message = document.createElement('div');
  message.className = `chat-message ${role === 'user' ? 'user-message' : 'assistant-message'}`;
  message.textContent = text;
  messages.append(message);
  messages.scrollTop = messages.scrollHeight;
}

launcher.addEventListener('click', () => setChatOpen(!panel.classList.contains('is-open')));
closeButton.addEventListener('click', () => setChatOpen(false));
document.querySelectorAll('[data-question]').forEach((button) => {
  button.addEventListener('click', () => {
    input.value = button.dataset.question;
    form.requestSubmit();
  });
});
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message) return;
  addMessage(message, 'user');
  input.value = '';
  input.disabled = true;
  form.querySelector('button').disabled = true;
  try {
    const response = await fetch('/api/chat/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
      body: JSON.stringify({ message }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Please try again in a moment.');
    modeLabel.textContent = data.mode === 'ai' ? 'AI-powered portfolio guide' : 'Portfolio guide · demo mode';
    addMessage(data.reply, 'assistant');
  } catch (error) {
    addMessage(error.message || 'I could not connect just now. Please try again.', 'assistant');
  } finally {
    input.disabled = false;
    form.querySelector('button').disabled = false;
    input.focus();
  }
});

function getCookie(name) {
  const cookie = document.cookie.split('; ').find((item) => item.startsWith(`${name}=`));
  return cookie ? decodeURIComponent(cookie.split('=').slice(1).join('=')) : '';
}