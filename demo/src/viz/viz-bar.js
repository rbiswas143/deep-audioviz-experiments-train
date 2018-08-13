import THREE from "../three";
import BaseViz from "./base-viz";

export default class VizBar extends BaseViz {
  constructor(container) {
    super(container);
    this.vizParams = {
      numBars: 10,
      maxBarSize: 50,
      paused: false,
    };
    this.animParams = {
      bar1: 0.9,
      bar2: 0.5,
      bar3: 0.6,
      bar4: 0.2,
      bar5: 0.7,
      bar6: 0.1,
      bar7: 0.3,
      bar8: 0.8,
      bar9: 0.03,
      bar10: 0.5
    };

    // Scene
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(
      40,
      container.offsetWidth / container.offsetHeight,
      0.1,
      20000
    );
    this.camera.position.set(0, 45, 0);

    this.renderer = new THREE.WebGLRenderer({
      antialias: true
    });
    this.renderer.setSize(
      this.container.offsetWidth,
      this.container.offsetHeight
    );
    this.renderer.setClearColor(0x333F47, 1);
    this.container.appendChild(this.renderer.domElement);

    const light = new THREE.PointLight(0xffffff);
    light.position.set(-100, 200, 100);
    this.scene.add(light);

    // Components
    this.createBars();

    // Orbit Controls
    this.initOrbitControls();

    // this.renderer.render(this.scene, this.camera);
  }

  static getVisualParamsInfo() {
    return [
      ['bar1', 'Bar 1 Length'],
      ['bar2', 'Bar 2 Length'],
      ['bar3', 'Bar 3 Length'],
      ['bar4', 'Bar 4 Length'],
      ['bar5', 'Bar 5 Length'],
      ['bar6', 'Bar 6 Length'],
      ['bar7', 'Bar 7 Length'],
      ['bar8', 'Bar 8 Length'],
      ['bar9', 'Bar 9 Length'],
      ['bar10', 'Bar 10 Lengtht']
    ]
  }

  getRandomColor() {
    const letters = '0123456789ABCDEF'.split('');
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }

  createBars() {
    this.bars = [];
    for (let i = 0; i < this.vizParams.numBars; i++) {
      const barGeometry = new THREE.BoxGeometry(0.5, 0.5, 0.5);
      const material = new THREE.MeshPhongMaterial({
        color: this.getRandomColor(),
        specular: 0xffffff
      });
      this.bars[i] = new THREE.Mesh(barGeometry, material);
      this.bars[i].position.set(i - this.vizParams.numBars / 2, 0, 0);
      this.scene.add(this.bars[i]);
    }
  }

  animate(time) {
    for (let i = 0; i < this.vizParams.numBars; i++) {
      this.bars[i].scale.z = this.animParams['bar' + (i + 1)] * this.vizParams.maxBarSize;
    }
  }

}