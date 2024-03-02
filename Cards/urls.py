from django.urls import path
from .views import CreateCategoryView, CreateSubjectView,AddCardCollectionView, SubjectsByCategoryView,AllCategoriesView, UserCollectionsView, UserCreatedCollectionsView, CreateCollectionView, CreateMultipleCardsView, CreateCardView

urlpatterns = [
    path('/category/new', CreateCategoryView.as_view()),
    path('/card/new', CreateCardView.as_view()),
    path('/cards/new', CreateMultipleCardsView.as_view()),
    path('/subject/new', CreateSubjectView.as_view()),
    path('/user/cardcollections', UserCollectionsView.as_view()),
    path('/my/cardcollections', UserCreatedCollectionsView.as_view(),),
    path('/cardcollection/new', CreateCollectionView.as_view()),
    path('/categories', AllCategoriesView.as_view()),
    path('/categories/<int:category_id>/subjects', SubjectsByCategoryView.as_view()),
    path('/add-cardcollection/<int:collection_id>', AddCardCollectionView.as_view(), name='add-cardcollection'),
]
