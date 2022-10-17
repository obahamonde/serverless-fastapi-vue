from typing import *
from fastapi import *
from fastapi.staticfiles import StaticFiles
from fastapi.responses import *
from pydantic import *
from mangum import Mangum

class App(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mount("/static", StaticFiles(directory="static"), name="static")
        
app = App()

VUE = """const { createApp, defineComponent, onMounted, onUnmounted, onUpdated, onBeforeMount,
        onBeforeUnmount,
        onBeforeUpdate,
        onActivated,
        onDeactivated,
        onErrorCaptured,
        onRenderTracked,
        onRenderTriggered,
        provide,
        inject,
        nextTick,
        h,
        toRefs,
        toRef,
        isRef,
        ref,
        unref,
        customRef,
        triggerRef,
        shallowRef,
        watch,
        watchEffect,
        watchPostEffect,
        watchSyncEffect,
        computed,
        isReactive,
        isReadonly,
        isProxy,
        markRaw,
        reactive,
        readonly,
        shallowReactive,
        shallowReadonly,
        toRaw
  } = Vue;
  """

render = lambda x : f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/@unocss/reset/tailwind.min.css"
    />
    <title>{x}</title>
  </head>

  <body>
    <div id="app"></div>
    <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@unocss/runtime"></script>
    <script>{VUE}</script>
    <script src='/static/{x}.js'></script>
  </body>
</html>
"""

@app.get("/{x}")
async def index(x: str):
    return HTMLResponse(render(x))

@app.get("/")
async def index():
    return "foo"


handler = Mangum(app)
