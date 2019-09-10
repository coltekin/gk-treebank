Jekyll::Hooks.register(:pages, :post_init) do |post|
  post.content = post.content.gsub(/\[u-pos\/([A-Z]+)\]\(\)/, '[\1](https://universaldependencies.org/u/pos/\1.html)')
end
