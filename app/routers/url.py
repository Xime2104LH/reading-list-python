from fastapi import APIRouter, Depends
from app.services.encryption_service import validate_jwt_token
from app.models.models import UrlCreateSchema, Url, UrlTags, ResponseGlobal, UrlTagsResponse, UpdateTagsBody
from app.db.database_setup import engine
from sqlmodel import Session, select
import uuid

router = APIRouter(
    prefix="/url",
    tags=["URL"]
)

def get_session():
    with Session(engine) as session:
        yield session

@router.get("/", status_code=200)
def get_urls(decoded_user: dict = Depends(validate_jwt_token), session: Session = Depends(get_session)):
    print(" decoded info user ", decoded_user)

    user_id = decoded_user.user_id
    urls = []
    if user_id:

        query = select(Url).where(Url.user_id == user_id)
        results = session.exec(query).all() # lista de objetos de Url
        urls = []
        for res in results:
            query_tags = select(UrlTags).where(UrlTags.url_id == res.id)
            tags = session.exec(query_tags).all()
            tags_list = []
            for tag in tags:
                tags_list.append(tag.name_tag)

            urls.append({
                "url": res.url,
                "tags": tags_list
            })

    return {
        "user_id": user_id,
        "urls_list": urls
    }

@router.post("/", status_code=201) # Pensar hacer relationships attributes más adelante
def add_url(body: UrlCreateSchema,  decoded_user: dict = Depends(validate_jwt_token), session: Session = Depends(get_session)):

    user_id = decoded_user.user_id

    if user_id:
        url = Url(url=body.url, user_id=user_id)
        session.add(url)
        session.commit()
        session.refresh(url)

        list_tags = body.tags
        for tag in list_tags:
            url_tag = UrlTags(url_id=url.id, name_tag=tag)
            session.add(url_tag)

        session.commit()

    return ResponseGlobal(success=True, message="Se agregó correctamente la Url a la lista", data=url)

@router.delete("/{url_id}")
def delete_url(url_id: uuid.UUID, session: Session = Depends(get_session), decoded_user : dict = Depends(validate_jwt_token)):
    url_found = session.exec(select(Url).where(Url.id == url_id)).one()
    if not url_found:
        raise ResponseGlobal(success=False, message="No se encontró la URL", data=None)

    tags_found = session.exec(select(UrlTags).where(UrlTags.url_id == url_id)).all()
    if tags_found:
        for tag in tags_found:
            session.delete(tag)
        session.commit()

    session.delete(url_found)
    session.commit()

    return ResponseGlobal(success=True, message="Eliminado correctamente", data=None)

@router.put("/{url_id}")
def update_tags_by_url(url_id: uuid.UUID, tags: UpdateTagsBody, session: Session = Depends(get_session), decoded_user: dict = Depends(validate_jwt_token)):
    url_found = session.exec(select(Url).where(Url.id == url_id)).one()

    if not url_found:
        raise ResponseGlobal(success=False, message="No se encontró la URL", data=None)
    
    tags_found = session.exec(select(UrlTags).where(UrlTags.url_id == url_id)).all()

    if tags_found:
        for tag in tags_found:
            session.delete(tag)
        session.commit()

    for tag in tags.tags:
        url_tag = UrlTags(url_id=url_id, name_tag=tag)
        print("url tag ", url_tag)
        session.add(url_tag)

    session.commit()

    return ResponseGlobal(success=True, message="Se actualizaron las tags correctamente", data=None)