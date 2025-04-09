def handle_mouse_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Clic sur barre d'inventaire
            for i in range(10):
                if self.is_mouse_on_slot(485 + i * 60, self.screen.get_height() - 90, 50, 50):
                    if self.inventory_bar_list[i]:
                        self.dragging_item = self.inventory_bar_list[i]
                        self.dragging_item['icon'] = self.inventory_icons[i]
                        self.drag_start_pos = ("bar", i)
                        self.inventory_bar_list[i] = {}
                        self.inventory_icons[i] = pygame.image.load("Items/slot.png")
                        self.stack_text[i] = self.font.render("", True, (255, 255, 255))

            # Clic sur sac
            for row in range(5):
                for col in range(6):
                    if self.is_mouse_on_slot(595 + col * (self.CELL_SIZE + self.CELL_SPACING),290 + row * (self.CELL_SIZE + self.CELL_SPACING),self.CELL_SIZE, self.CELL_SIZE):
                        if self.inventory_list[row][col]:
                            self.dragging_item = self.inventory_list[row][col]
                            self.dragging_item['icon'] = self.inventory_bag_icon[row][col]
                            self.drag_start_pos = ("bag", row, col)
                            self.inventory_list[row][col] = {}
                            self.inventory_bag_icon[row][col] = pygame.image.load("Items/slot.png")
                            self.inventory_bag_stack_text[row][col] = self.font.render("", True, (255, 255, 255))

            # Clic sur armure
            if self.OnArmour:
                for i in range(len(self.armour_list)):
                    if self.is_mouse_on_slot(800, 288 + i * 70, 50, 50):
                        if self.armour_list[i]:
                            self.dragging_item = self.armour_list[i]
                            self.dragging_item['icon'] = self.armour_icon_list[i]
                            self.drag_start_pos = ("armour", i)
                            self.armour_list[i] = {}
                            self.armour_icon_list[i] = self.armour_icon_list2[i]
                

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if self.OnBag:
                # Déposer dans barre
                for i in range(10):
                    if self.is_mouse_on_slot(485 + i * 60, self.screen.get_height() - 90, 50, 50):
                        if self.dragging_item:
                            slot = self.inventory_bar_list[i]
                            if slot and slot['name'] == self.dragging_item['name']:
                                total = slot['quantity'] + self.dragging_item['quantity']
                                stack_max = slot['object'].stack_max
                                if total <= stack_max:
                                    slot['quantity'] = total
                                    self.stack_text[i] = self.font.render(str(total), True, (255, 255, 255))
                                    self.dragging_item = None
                                    self.drag_start_pos = None
                                    return
                            # Sinon échange
                            if slot:
                                temp, temp_icon, temp_text = slot, self.inventory_icons[i], self.stack_text[i]
                                origin = self.drag_start_pos
                                if origin[0] == "bar":
                                    self.inventory_bar_list[origin[1]] = temp
                                    self.inventory_icons[origin[1]] = temp_icon
                                    self.stack_text[origin[1]] = temp_text
                                elif origin[0] == "bag":
                                    self.inventory_list[origin[1]][origin[2]] = temp
                                    self.inventory_bag_icon[origin[1]][origin[2]] = temp_icon
                                    self.inventory_bag_stack_text[origin[1]][origin[2]] = temp_text
                                elif origin[0] == "armour":
                                    self.armour_list[origin[1]] = temp
                                    self.armour_icon_list[origin[1]] = temp_icon

                            self.inventory_bar_list[i] = self.dragging_item
                            self.inventory_icons[i] = self.dragging_item['icon']
                            self.stack_text[i] = self.font.render(str(self.dragging_item['quantity']), True, (255, 255, 255))
                            self.dragging_item = None
                            self.drag_start_pos = None
                            break

                # Déposer dans sac
                for row in range(5):
                    for col in range(6):
                        if self.is_mouse_on_slot(595 + col * (self.CELL_SIZE + self.CELL_SPACING),
                                                290 + row * (self.CELL_SIZE + self.CELL_SPACING),
                                                self.CELL_SIZE, self.CELL_SIZE):
                            if self.dragging_item:
                                slot = self.inventory_list[row][col]
                                if slot and slot['name'] == self.dragging_item['name']:
                                    total = slot['quantity'] + self.dragging_item['quantity']
                                    stack_max = slot['object'].stack_max
                                    if total <= stack_max:
                                        slot['quantity'] = total
                                        self.inventory_bag_stack_text[row][col] = self.font.render(str(total), True, (255, 255, 255))
                                        self.dragging_item = None
                                        self.drag_start_pos = None
                                        return
                                # Sinon on échange
                                if slot:
                                    temp, temp_icon, temp_text = slot, self.inventory_bag_icon[row][col], self.inventory_bag_stack_text[row][col]
                                    origin = self.drag_start_pos
                                    if origin[0] == "bar":
                                        self.inventory_bar_list[origin[1]] = temp
                                        self.inventory_icons[origin[1]] = temp_icon
                                        self.stack_text[origin[1]] = temp_text
                                    elif origin[0] == "bag":
                                        self.inventory_list[origin[1]][origin[2]] = temp
                                        self.inventory_bag_icon[origin[1]][origin[2]] = temp_icon
                                        self.inventory_bag_stack_text[origin[1]][origin[2]] = temp_text
                                    elif origin[0] == "armour":
                                        self.armour_list[origin[1]] = temp
                                        self.armour_icon_list[origin[1]] = temp_icon

                                self.inventory_list[row][col] = self.dragging_item
                                self.inventory_bag_icon[row][col] = self.dragging_item['icon']
                                self.inventory_bag_stack_text[row][col] = self.font.render(str(self.dragging_item['quantity']), True, (255, 255, 255))
                                self.dragging_item = None
                                self.drag_start_pos = None
                                break
                # Si on a relâché en dehors de tout slot, on remet l'objet à sa place d'origine
                if self.dragging_item and self.drag_start_pos:
                    origin = self.drag_start_pos
                    if origin[0] == "bar":
                        self.inventory_bar_list[origin[1]] = self.dragging_item
                        self.inventory_icons[origin[1]] = self.dragging_item['icon']
                        self.stack_text[origin[1]] = self.font.render(str(self.dragging_item['quantity']), True, (255, 255, 255))
                    elif origin[0] == "bag":
                        self.inventory_list[origin[1]][origin[2]] = self.dragging_item
                        self.inventory_bag_icon[origin[1]][origin[2]] = self.dragging_item['icon']
                        self.inventory_bag_stack_text[origin[1]][origin[2]] = self.font.render(str(self.dragging_item['quantity']), True, (255, 255, 255))
                    elif origin[0] == "armour":
                        self.armour_list[origin[1]] = self.dragging_item
                        self.armour_icon_list[origin[1]] = self.dragging_item['icon']
                    self.dragging_item = None
                    self.drag_start_pos = None

            # Déposer dans armure
            if self.OnArmour:
                for i in range(len(self.armour_list)):
                    if self.is_mouse_on_slot(800, 288 + i * 70, 50, 50):
                        if self.dragging_item:
                            # Vérifier si l'objet est du bon type pour l'emplacement
                            if (i == 0 and self.dragging_item['object'].type == "Casque") or \
                            (i == 1 and self.dragging_item['object'].type == "Plastron") or \
                            (i == 2 and self.dragging_item['object'].type == "Jambiere") or \
                            (i == 3 and self.dragging_item['object'].type == "Bottes"):
                                slot = self.armour_list[i]
                                if slot and slot['name'] == self.dragging_item['name']:
                                    total = slot['quantity'] + self.dragging_item['quantity']
                                    stack_max = slot['object'].stack_max
                                    if total <= stack_max:
                                        slot['quantity'] = total
                                        self.armour_icon_list[i] = self.font.render(str(total), True, (255, 255, 255))
                                        self.dragging_item = None
                                        self.drag_start_pos = None
                                        return
                                # Sinon échange
                                if slot:
                                    temp, temp_icon = slot, self.armour_icon_list[i]
                                    origin = self.drag_start_pos
                                    if origin[0] == "bar":
                                        self.inventory_bar_list[origin[1]] = temp
                                        self.inventory_icons[origin[1]] = temp_icon
                                    elif origin[0] == "bag":
                                        self.inventory_list[origin[1]][origin[2]] = temp
                                        self.inventory_bag_icon[origin[1]][origin[2]] = temp_icon
                                    elif origin[0] == "armour":
                                        self.armour_list[origin[1]] = temp
                                        self.armour_icon_list[origin[1]] = temp_icon

                                self.armour_list[i] = self.dragging_item
                                self.armour_icon_list[i] = self.dragging_item['icon']
                                self.dragging_item = None
                                self.drag_start_pos = None
                                break
                            else:
                                # Remettre l'objet à sa place d'origine s'il n'est pas du bon type
                                origin = self.drag_start_pos
                                if origin[0] == "bar":
                                    self.inventory_bar_list[origin[1]] = self.dragging_item
                                    self.inventory_icons[origin[1]] = self.dragging_item['icon']
                                    self.stack_text[origin[1]] = self.font.render(str(self.dragging_item['quantity']), True, (255, 255, 255))
                                elif origin[0] == "bag":
                                    self.inventory_list[origin[1]][origin[2]] = self.dragging_item
                                    self.inventory_bag_icon[origin[1]][origin[2]] = self.dragging_item['icon']
                                    self.inventory_bag_stack_text[origin[1]][origin[2]] = self.font.render(str(self.dragging_item['quantity']), True, (255, 255, 255))
                                elif origin[0] == "armour":
                                    self.armour_list[origin[1]] = self.dragging_item
                                    self.armour_icon_list[origin[1]] = self.dragging_item['icon']
                                self.dragging_item = None
                                self.drag_start_pos = None

            # Déposer depuis l'armure vers la barre d'inventaire
            if self.drag_start_pos and self.drag_start_pos[0] == "armour":
                item_returned = False
                for i in range(10):
                    if self.is_mouse_on_slot(485 + i * 60, self.screen.get_height() - 90, 50, 50):
                        if self.dragging_item:
                            slot = self.inventory_bar_list[i]
                            if slot and slot['name'] == self.dragging_item['name']:
                                total = slot['quantity'] + self.dragging_item['quantity']
                                stack_max = slot['object'].stack_max
                                if total <= stack_max:
                                    slot['quantity'] = total
                                    self.stack_text[i] = self.font.render(str(total), True, (255, 255, 255))
                                    self.dragging_item = None
                                    self.drag_start_pos = None
                                    return
                            # Sinon échange
                            if slot:
                                temp, temp_icon, temp_text = slot, self.inventory_icons[i], self.stack_text[i]
                                origin = self.drag_start_pos
                                if origin[0] == "bar":
                                    self.inventory_bar_list[origin[1]] = temp
                                    self.inventory_icons[origin[1]] = temp_icon
                                    self.stack_text[origin[1]] = temp_text
                                elif origin[0] == "bag":
                                    self.inventory_list[origin[1]][origin[2]] = temp
                                    self.inventory_bag_icon[origin[1]][origin[2]] = temp_icon
                                    self.inventory_bag_stack_text[origin[1]][origin[2]] = temp_text
                                elif origin[0] == "armour":
                                    self.armour_list[origin[1]] = temp
                                    self.armour_icon_list[origin[1]] = temp_icon

                            self.inventory_bar_list[i] = self.dragging_item
                            self.inventory_icons[i] = self.dragging_item['icon']
                            self.stack_text[i] = self.font.render(str(self.dragging_item['quantity']), True, (255, 255, 255))
                            self.dragging_item = None
                            self.drag_start_pos = None
                            item_returned = True
                            break

                # Si aucun slot n'est atteint, remettre l'objet à sa place d'origine
                if not item_returned and self.drag_start_pos:
                    origin = self.drag_start_pos
                    if origin[0] == "armour":
                        self.armour_list[origin[1]] = self.dragging_item
                        self.armour_icon_list[origin[1]] = self.dragging_item['icon']
                    self.dragging_item = None
                    self.drag_start_pos = None