declare module 'ogl' {
    export class Renderer {
        constructor(options?: { dpr?: number, canvas?: HTMLCanvasElement, width?: number, height?: number, webgl?: number, alpha?: boolean, depth?: boolean, stencil?: boolean, antialias?: boolean, premultipliedAlpha?: boolean, preserveDrawingBuffer?: boolean, powerPreference?: string, autoClear?: boolean });
        gl: WebGLRenderingContext | WebGL2RenderingContext;
        setSize(width: number, height: number): void;
        render(options: { scene: Transform | Mesh, camera?: Camera }): void;
    }

    export class Program {
        constructor(gl: WebGLRenderingContext | WebGL2RenderingContext, options?: { vertex?: string, fragment?: string, uniforms?: { [key: string]: { value: any } }, transparent?: boolean, culling?: number, depthTest?: boolean, depthWrite?: boolean, depthFunc?: number });
        uniforms: { [key: string]: { value: any } };
    }

    export class Mesh {
        constructor(gl: WebGLRenderingContext | WebGL2RenderingContext, options?: { geometry: Geometry, program: Program });
    }

    export class Triangle {
        constructor(gl: WebGLRenderingContext | WebGL2RenderingContext, options?: { attributes?: { [key: string]: any } });
    }

    export class Vec2 {
        constructor(x?: number, y?: number);
        set(x: number, y: number): this;
        value: Float32Array;
    }

    export class Transform {
        constructor();
    }

    export class Camera extends Transform {
        constructor(gl: WebGLRenderingContext | WebGL2RenderingContext, options?: { fov?: number, aspect?: number, near?: number, far?: number });
    }

    export class Geometry {
        constructor(gl: WebGLRenderingContext | WebGL2RenderingContext, attributes?: { [key: string]: any });
    }
}
