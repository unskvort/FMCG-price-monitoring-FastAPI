from typing import Any, Type

from sqlmodel import Session, SQLModel, select


class Crud:
    @classmethod
    def get_objects(
        cls, session: Session, model: Type[SQLModel], limit: int | None = None, offset: int | None = None
    ) -> list[Any]:
        instance = session.execute(select(model).offset(offset).limit(limit))
        result = instance.scalars().all()
        return result

    @classmethod
    def get_object(  # type: ignore
        cls,
        session: Session,
        model: Type[SQLModel],
        many: bool = False,
        **kwargs,
    ) -> list[Any] | None:
        if many:
            instance = session.execute(select(model).filter_by(**kwargs)).scalars().all()
        else:
            instance = session.execute(select(model).filter_by(**kwargs)).scalar()  # type: ignore
        if instance:
            return instance
        else:
            return None

    @classmethod
    def create_object(cls, session: Session, model: Type[SQLModel], **kwargs) -> Any:  # type: ignore
        instance = model(**kwargs)
        cls.save(session, instance)
        return instance

    @classmethod
    def get_or_create(cls, session: Session, model: Type[SQLModel], **kwargs) -> Type[SQLModel]:  # type: ignore
        if "article" in kwargs.keys():
            instance = session.execute(select(model).filter_by(article=kwargs["article"])).scalar()
        else:
            instance = cls.get_object(session, model, **kwargs)
        if instance:
            return instance
        else:
            instance = cls.create_object(session, model, **kwargs)
            return instance

    @classmethod
    def save(cls, session: Session, obj: Any = None) -> None:
        session.add(obj)
        session.commit()
        session.refresh(obj)


crud = Crud()
