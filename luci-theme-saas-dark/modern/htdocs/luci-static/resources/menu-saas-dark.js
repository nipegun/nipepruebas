'use strict';
'require baseclass';
'require ui';

return baseclass.extend({
  __init__: function() {
    ui.menu.load().then(L.bind(function(tree) {
      this.render(tree);
    }, this));
  },

  render: function(tree) {
    var node = tree;
    var url = '';

    this.renderModeMenu(tree);

    if (L.env.dispatchpath.length >= 3) {
      for (var i = 0; i < 3 && node; i++) {
        node = node.children[L.env.dispatchpath[i]];
        url = url + (url ? '/' : '') + L.env.dispatchpath[i];
      }

      if (node)
        this.renderTabMenu(node, url);
    }
  },

  renderTabMenu: function(tree, url, level) {
    var container = document.querySelector('#tabmenu');
    var ul = E('ul', { 'class': 'tabs' });
    var children = ui.menu.getChildren(tree);
    var activeNode = null;

    children.forEach(function(child) {
      var isActive = (L.env.dispatchpath[3 + (level || 0)] == child.name);
      var activeClass = isActive ? ' active' : '';
      var className = 'tabmenu-item-' + child.name + activeClass;

      ul.appendChild(E('li', { 'class': className }, [
        E('a', { 'href': L.url(url, child.name) }, [ _(child.title) ])
      ]));

      if (isActive)
        activeNode = child;
    });

    if (ul.children.length == 0)
      return E([]);

    container.appendChild(ul);
    container.style.display = '';

    if (activeNode)
      this.renderTabMenu(activeNode, url + '/' + activeNode.name, (level || 0) + 1);

    return ul;
  },

  renderMainMenu: function(tree, url, level) {
    var ul = document.querySelector('#topmenu');
    var children = ui.menu.getChildren(tree);

    if (children.length == 0)
      return E([]);

    var self = this;
    var activeL2 = L.env.dispatchpath[1] || '';

    children.forEach(function(child) {
      var isActive = (child.name === activeL2);
      var submenu = self.renderSubMenu(child, url + '/' + child.name);
      var hasChildren = submenu && submenu.children && submenu.children.length > 0;

      var li = E('li', {
        'class': 'menu-item' + (isActive ? ' active' : '') + (hasChildren ? ' has-children' : '')
      });

      var link = E('a', {
        'class': 'menu-link',
        'href': hasChildren ? '#' : L.url(url, child.name)
      }, [
        E('span', { 'class': 'menu-icon' }),
        E('span', { 'class': 'menu-text' }, [ _(child.title) ])
      ]);

      if (hasChildren) {
        var chevron = E('span', { 'class': 'menu-chevron' });
        link.appendChild(chevron);

        link.addEventListener('click', function(ev) {
          ev.preventDefault();
          li.classList.toggle('open');
        });
      }

      li.appendChild(link);

      if (hasChildren) {
        li.appendChild(submenu);
        if (isActive) {
          li.classList.add('open');
        }
      }

      ul.appendChild(li);
    });

    ul.style.display = '';

    return ul;
  },

  renderSubMenu: function(tree, url) {
    var children = ui.menu.getChildren(tree);

    if (children.length == 0)
      return E([]);

    var ul = E('ul', { 'class': 'menu-sub' });
    var activeL3 = L.env.dispatchpath[2] || '';

    children.forEach(function(child) {
      var isActive = (child.name === activeL3);
      ul.appendChild(E('li', { 'class': 'menu-sub-item' + (isActive ? ' active' : '') }, [
        E('a', { 'href': L.url(url, child.name) }, [ _(child.title) ])
      ]));
    });

    return ul;
  },

  renderModeMenu: function(tree) {
    var ul = document.querySelector('#modemenu');
    var children = ui.menu.getChildren(tree);
    var self = this;

    children.forEach(function(child, index) {
      var isActive = L.env.requestpath.length
        ? child.name === L.env.requestpath[0]
        : index === 0;

      ul.appendChild(E('li', { 'class': isActive ? 'active' : '' }, [
        E('a', { 'href': L.url(child.name) }, [ _(child.title) ])
      ]));

      if (isActive)
        self.renderMainMenu(child, child.name);
    });

    if (ul.children.length > 1)
      ul.style.display = '';
  }
});
