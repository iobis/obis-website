module Jekyll
  class TagPage < Page
    def initialize(site, base, dir, tag, slug)
      @site = site
      @base = base
      @dir = dir
      @name = 'index.html'

      self.process(@name)
      self.read_yaml(File.join(base, '_layouts'), 'tag.html')
      self.data['tag'] = tag
      self.data['slug'] = slug
      self.data['title'] = "Posts tagged with \"#{tag}\""
      self.data['permalink'] = "/tag/#{slug}/"
    end
  end

  class TagGenerator < Generator
    safe true

    def slugify(tag)
      tag.downcase.strip.gsub(' ', '-').gsub(/[^\w-]/, '')
    end

    def generate(site)
      all_docs = site.posts.docs
      if site.collections.key?('usecases')
        all_docs += site.collections['usecases'].docs
      end

      # Group tags by their slugified version (case-insensitive)
      tag_groups = {}
      all_docs.each do |doc|
        (doc.data['tags'] || []).each do |tag|
          slug = slugify(tag)
          tag_groups[slug] ||= tag  # Keep first occurrence of tag for display
        end
      end

      tag_groups.each do |slug, tag|
        site.pages << TagPage.new(site, site.source, File.join('tag', slug), tag, slug)
      end
    end
  end
end