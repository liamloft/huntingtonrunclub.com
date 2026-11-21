import asyncio, base64, sys, os, time
from playwright.async_api import async_playwright
kind=sys.argv[1]; n=int(sys.argv[2]); frames=[int(x) for x in sys.argv[3].split(",")] if len(sys.argv)>3 and sys.argv[3]!="all" else None
size=int(os.environ.get("SIZE","1200")); out=f"frames_{kind}"; os.makedirs(out,exist_ok=True)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-gl=angle","--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist"])
        pg = await b.new_page(viewport={"width":size,"height":size})
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
        await pg.goto(f"http://localhost:8765/render.html?kind={kind}&size={size}")
        await pg.wait_for_function("window.ready===true", timeout=120000)
        t0=time.time()
        for i in (frames if frames is not None else range(n)):
            d = await pg.evaluate(f"renderFrame({i},{n})")
            open(f"{out}/f{i:03d}.png","wb").write(base64.b64decode(d.split(",")[1]))
        print(kind, "done", round(time.time()-t0,1), "s", errs[:3])
        await b.close()
asyncio.run(main())
