from fastapi import FastAPI, Request, Form, Path
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
import uvicorn

from models.services import SERVICES, SERVICE_BACKGROUNDS

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


def add_template_filters(env):
    # Add filters if needed
    pass


templates.env.globals["enumerate"] = enumerate  # Make enumerate available in templates
templates.env.globals["SERVICE_BACKGROUNDS"] = (
    SERVICE_BACKGROUNDS  # Make backgrounds available in templates
)


# region Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page."""
    return templates.TemplateResponse(
        "pages/home.html",
        {
            "request": request,
            "services": SERVICES[:6],
            "SERVICE_BACKGROUNDS": SERVICE_BACKGROUNDS,
        },
    )


@app.get("/ueber-uns", response_class=HTMLResponse)
async def about(request: Request):
    """Render the about page."""
    return templates.TemplateResponse("pages/about.html", {"request": request})


@app.get("/leistungen", response_class=HTMLResponse)
async def services(request: Request):
    """Render the services page."""
    return templates.TemplateResponse(
        "pages/services.html",
        {
            "request": request,
            "services": SERVICES,
            "SERVICE_BACKGROUNDS": SERVICE_BACKGROUNDS,
        },
    )


@app.get("/kontakt", response_class=HTMLResponse)
async def contact(request: Request):
    """Render the contact page."""
    return templates.TemplateResponse("pages/contact.html", {"request": request})


@app.post("/api/toggle-menu", response_class=HTMLResponse)
async def toggle_menu():
    """Toggle is-active class for navbar burger and menu"""
    return "is-active"


@app.get("/static/{path:path}")
async def get_static(path: str):
    """
    Serve static files from the static directory with appropriate MIME types.

    Args:
        path: The path to the static file

    Returns:
        FileResponse: The file response with the correct MIME type
    """
    file_path = f"static/{path}"

    # Determine MIME type based on file extension
    mime_types = {
        "css": "text/css",
        "js": "application/javascript",
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "gif": "image/gif",
        "svg": "image/svg+xml",
        "ico": "image/x-icon",
        "woff": "font/woff",
        "woff2": "font/woff2",
        "ttf": "font/ttf",
        "otf": "font/otf",
    }

    # Get file extension
    ext = path.split(".")[-1].lower() if "." in path else ""

    # Set media_type if known
    media_type = mime_types.get(ext)

    return FileResponse(file_path, media_type=media_type)


@app.get("/api/service/{id}", response_class=HTMLResponse)
async def get_service(request: Request, id: int = Path(...)):
    """
    HTMX endpoint to get service details with custom background styling.

    Args:
        request:
        id: Service ID to retrieve details for

    Returns:
        HTML: Expanded service content with background styling
    """
    service_id = int(id)
    service = next((s for s in SERVICES if s["id"] == service_id), None)

    if not service:
        return "Service nicht gefunden"

    return templates.TemplateResponse(
        "partials/service_content.html",
        {"request": request, "service": service, "is_expanded": True},
    )


@app.get("/api/service/{id}/close", response_class=HTMLResponse)
async def close_service(request: Request, id: int = Path(...)):
    """
    HTMX endpoint to restore the original card content when closing expanded view.

    Args:
        request:
        id: Service ID to close and return to preview state


    Returns:
        HTML: Collapsed service preview with background styling
    """
    service_id = int(id)
    service = next((s for s in SERVICES if s["id"] == service_id), None)

    if not service:
        return "Service nicht gefunden"

    return templates.TemplateResponse(
        "partials/service_content.html",
        {"request": request, "service": service, "is_expanded": False},
    )


@app.post("/api/submit-contact", response_class=HTMLResponse)
async def submit_contact(
    request: Request,
    salutation: Optional[str] = Form(None),
    name: str = Form(...),
    email: str = Form(...),
    phone: Optional[str] = Form(None),
    subject: str = Form(...),
    message: str = Form(...),
    privacy: bool = Form(...),
):
    """Handle contact form submission."""
    # TODO: Implement contact form submission
    return templates.TemplateResponse(
        "partials/contact_response.html",
        {"request": request, "success": True, "name": name},
    )


# endregion

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
