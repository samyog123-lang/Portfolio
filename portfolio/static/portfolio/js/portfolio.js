const canvas = document.querySelector('#hero-canvas');
const menuToggle = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#primary-navigation');

menuToggle?.addEventListener('click', () => {
  const isOpen = menuToggle.getAttribute('aria-expanded') === 'true';
  menuToggle.setAttribute('aria-expanded', String(!isOpen));
  menuToggle.setAttribute('aria-label', isOpen ? 'Open navigation' : 'Close navigation');
  navigation.classList.toggle('is-open', !isOpen);
});

navigation?.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => {
    navigation.classList.remove('is-open');
    menuToggle?.setAttribute('aria-expanded', 'false');
    menuToggle?.setAttribute('aria-label', 'Open navigation');
  });
});

document.querySelectorAll('[data-project-filter]').forEach((button) => {
  button.addEventListener('click', () => {
    const filter = button.dataset.projectFilter;
    document.querySelectorAll('[data-project-filter]').forEach((filterButton) => {
      filterButton.classList.toggle('is-active', filterButton === button);
    });
    document.querySelectorAll('.project-card[data-project-category]').forEach((card) => {
      card.classList.toggle('is-filtered', filter !== 'all' && card.dataset.projectCategory !== filter);
    });
  });
});

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });
document.querySelectorAll('.content-section, .project-card, .journey-item').forEach((element, index) => {
  element.classList.add('reveal');
  element.style.setProperty('--reveal-delay', `${Math.min(index % 3, 2) * 70}ms`);
  revealObserver.observe(element);
});

function getCookie(name) {
  const cookie = document.cookie.split('; ').find((item) => item.startsWith(`${name}=`));
  return cookie ? decodeURIComponent(cookie.split('=').slice(1).join('=')) : '';
}

async function submitAdminMessage(event, statusId) {
  event.preventDefault();
  const form = event.currentTarget;
  const values = new FormData(form);
  const payload = {
    channel: form.dataset.channel,
    name: values.get('name'),
    email: values.get('email') || '',
    subject: values.get('subject') || '',
    message: values.get('message'),
    website: values.get('website') || '',
  };
  const status = document.querySelector(`#${statusId}`);
  const button = form.querySelector('button[type="submit"]');
  status.textContent = 'Sending securely to the admin inbox…';
  button.disabled = true;

  try {
    const response = await fetch('/api/contact/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
      body: JSON.stringify(payload),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || 'Please try again.');
    status.textContent = result.message;
    form.reset();
  } catch (error) {
    status.textContent = error.message || 'Could not send your message. Please try again.';
  } finally {
    button.disabled = false;
  }
}

document.querySelector('#contact-form')?.addEventListener('submit', (event) => submitAdminMessage(event, 'contact-status'));
document.querySelector('#sms-form')?.addEventListener('submit', (event) => submitAdminMessage(event, 'sms-status'));

const launcher = document.querySelector('#chat-launcher');
const panel = document.querySelector('#chat-panel');
const closeButton = document.querySelector('#chat-close');
const chatForm = document.querySelector('#chat-form');
const chatInput = document.querySelector('#chat-input');
const chatMessages = document.querySelector('#chat-messages');
const chatMode = document.querySelector('#chat-mode');

function setChatOpen(open) {
  panel.classList.toggle('is-open', open);
  panel.setAttribute('aria-hidden', String(!open));
  launcher.setAttribute('aria-expanded', String(open));
  if (open) chatInput.focus();
}

function addChatMessage(text, role) {
  const message = document.createElement('div');
  message.className = `chat-message ${role === 'user' ? 'user-message' : 'assistant-message'}`;
  message.textContent = text;
  chatMessages.append(message);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

launcher?.addEventListener('click', () => setChatOpen(!panel.classList.contains('is-open')));
closeButton?.addEventListener('click', () => setChatOpen(false));
document.querySelectorAll('[data-question]').forEach((button) => {
  button.addEventListener('click', () => {
    chatInput.value = button.dataset.question;
    chatForm.requestSubmit();
  });
});
chatForm?.addEventListener('submit', async (event) => {
  event.preventDefault();
  const message = chatInput.value.trim();
  if (!message) return;
  addChatMessage(message, 'user');
  chatInput.value = '';
  chatInput.disabled = true;
  chatForm.querySelector('button').disabled = true;
  try {
    const response = await fetch('/api/chat/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
      body: JSON.stringify({ message }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Please try again in a moment.');
    chatMode.textContent = data.mode === 'ai' ? 'Samyog AI · verified portfolio context' : 'Verified portfolio information';
    addChatMessage(data.reply, 'assistant');
  } catch (error) {
    addChatMessage(error.message || 'The assistant could not connect. Please try again.', 'assistant');
  } finally {
    chatInput.disabled = false;
    chatForm.querySelector('button').disabled = false;
    chatInput.focus();
  }
});

if (canvas) {
  try {
    const THREE = await import('https://cdn.jsdelivr.net/npm/three@0.169.0/build/three.module.js');
    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true, preserveDrawingBuffer: true });
    const smallScreen = window.matchMedia('(max-width: 700px)').matches;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, smallScreen ? 1 : 1.4));
    renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.12;

    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x100d0e, 0.018);
    const camera = new THREE.PerspectiveCamera(36, canvas.clientWidth / canvas.clientHeight, 0.1, 100);
    camera.position.set(0.2, 2.1, 8.8);
    camera.lookAt(0, 0, 0);
    scene.add(new THREE.HemisphereLight(0xf7e8e4, 0x201012, 2.2));
    const keyLight = new THREE.DirectionalLight(0xffe8e0, 4);
    keyLight.position.set(-3, 6, 5);
    scene.add(keyLight);
    const redLight = new THREE.PointLight(0xf0443d, 31, 13);
    redLight.position.set(-2.6, 1.5, 3);
    scene.add(redLight);
    const greenLight = new THREE.PointLight(0x55bf8d, 18, 11);
    greenLight.position.set(2.8, -0.5, 2);
    scene.add(greenLight);

    const grid = new THREE.GridHelper(18, 32, 0x713437, 0x382326);
    grid.position.y = -1.72;
    grid.material.transparent = true;
    grid.material.opacity = 0.55;
    scene.add(grid);

    const world = new THREE.Group();
    scene.add(world);
    const server = new THREE.Group();
    server.position.set(-0.55, -0.05, 0);
    world.add(server);
    const chassisMaterial = new THREE.MeshPhysicalMaterial({ color: 0x21191b, metalness: 0.72, roughness: 0.27, clearcoat: 0.7 });
    const edgeMaterial = new THREE.LineBasicMaterial({ color: 0xe04b45, transparent: true, opacity: 0.72 });
    const addPanel = (width, height, depth, x, y, z, material = chassisMaterial) => {
      const mesh = new THREE.Mesh(new THREE.BoxGeometry(width, height, depth), material);
      mesh.position.set(x, y, z);
      server.add(mesh);
      const outline = new THREE.LineSegments(new THREE.EdgesGeometry(mesh.geometry), edgeMaterial);
      outline.position.copy(mesh.position);
      server.add(outline);
    };
    addPanel(1.65, 2.8, 1.05, 0, 0, 0);
    const shelfMaterial = new THREE.MeshStandardMaterial({ color: 0x48272a, metalness: 0.48, roughness: 0.34 });
    const ledMaterial = new THREE.MeshBasicMaterial({ color: 0xff6c62 });
    const greenLedMaterial = new THREE.MeshBasicMaterial({ color: 0x72d39a });
    for (let row = 0; row < 4; row += 1) {
      const y = -0.91 + row * 0.59;
      const shelf = new THREE.Mesh(new THREE.BoxGeometry(1.35, 0.43, 0.12), shelfMaterial);
      shelf.position.set(0, y, 0.57);
      server.add(shelf);
      for (let light = 0; light < 3; light += 1) {
        const dot = new THREE.Mesh(new THREE.SphereGeometry(0.035, 12, 12), light === 0 && row === 2 ? greenLedMaterial : ledMaterial);
        dot.position.set(-0.47 + light * 0.14, y, 0.65);
        server.add(dot);
      }
    }

    const database = new THREE.Group();
    database.position.set(2.05, -0.35, -0.45);
    world.add(database);
    const databaseMaterial = new THREE.MeshPhysicalMaterial({ color: 0x742e31, metalness: 0.36, roughness: 0.24, transparent: true, opacity: 0.82, clearcoat: 1 });
    const cylinder = new THREE.Mesh(new THREE.CylinderGeometry(0.78, 0.78, 1.55, 48, 1, false), databaseMaterial);
    database.add(cylinder);
    const cylinderEdges = new THREE.LineSegments(new THREE.EdgesGeometry(cylinder.geometry), new THREE.LineBasicMaterial({ color: 0xff9389, transparent: true, opacity: 0.65 }));
    database.add(cylinderEdges);
    const databaseRing = new THREE.Mesh(new THREE.TorusGeometry(0.79, 0.025, 8, 64), new THREE.MeshBasicMaterial({ color: 0xff827a }));
    databaseRing.position.y = 0.52;
    database.add(databaseRing);

    const orbit = new THREE.Mesh(new THREE.TorusGeometry(2.25, 0.012, 5, 180), new THREE.MeshBasicMaterial({ color: 0xff665f, transparent: true, opacity: 0.55 }));
    orbit.rotation.set(1.05, 0.1, -0.25);
    orbit.position.set(0.1, 0.05, -0.15);
    world.add(orbit);
    const secondOrbit = orbit.clone();
    secondOrbit.material = orbit.material.clone();
    secondOrbit.material.color.set(0x78c996);
    secondOrbit.material.opacity = 0.34;
    secondOrbit.scale.setScalar(1.27);
    secondOrbit.rotation.set(0.78, -0.44, 0.4);
    world.add(secondOrbit);

    const dataMaterial = new THREE.MeshStandardMaterial({ color: 0xff8378, emissive: 0x561817, metalness: 0.25, roughness: 0.25 });
    const dataNodes = [];
    const nodeCount = smallScreen ? 6 : 9;
    for (let index = 0; index < nodeCount; index += 1) {
      const node = new THREE.Mesh(new THREE.SphereGeometry(index % 3 === 0 ? 0.075 : 0.045, 16, 16), dataMaterial);
      node.userData.phase = (index / nodeCount) * Math.PI * 2;
      node.userData.radius = 2.15 + (index % 3) * 0.27;
      world.add(node);
      dataNodes.push(node);
    }

    const floaters = [];
    [[-2.7, 1.2, -0.7, 0.22, 0x3e84a5], [2.8, 1.4, -1.2, 0.16, 0xf0443d], [1.1, 2.05, 0.2, 0.12, 0x59b983]].forEach(([x, y, z, size, color]) => {
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
    new ResizeObserver(resize).observe(canvas);
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