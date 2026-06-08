Rails.application.routes.draw do
  resources :articles do
    resources :comments, only: [:create, :destroy]
  end

  root 'articles#index'
end
