<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" simplifyAlgorithm="0" hasScaleBasedVisibilityFlag="0" simplifyDrawingTol="1" version="3.12.3-București" minScale="100000000" labelsEnabled="0" readOnly="0" maxScale="0" simplifyLocal="1" simplifyDrawingHints="0" simplifyMaxScale="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" enableorderby="0" type="singleSymbol" symbollevels="0">
    <symbols>
      <symbol name="0" alpha="1" type="marker" clip_to_extent="1" force_rhr="0">
        <layer class="SvgMarker" locked="0" enabled="1" pass="0">
          <prop v="0" k="angle"/>
          <prop v="35,35,35,255" k="color"/>
          <prop v="0" k="fixedAspectRatio"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="strike-000-E.svg" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,255" k="outline_color"/>
          <prop v="0.2" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="2" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="angle" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="&quot;azimuth&quot; -90" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory backgroundAlpha="255" minimumSize="0" penWidth="0" maxScaleDenominator="1e+08" diagramOrientation="Up" sizeType="MM" height="15" penAlpha="255" spacingUnitScale="3x:0,0,0,0,0,0" enabled="0" spacing="5" labelPlacementMethod="XHeight" minScaleDenominator="0" opacity="1" showAxis="1" sizeScale="3x:0,0,0,0,0,0" penColor="#000000" direction="0" scaleBasedVisibility="0" width="15" barWidth="5" spacingUnit="MM" lineSizeType="MM" lineSizeScale="3x:0,0,0,0,0,0" rotationOffset="270" scaleDependency="Area" backgroundColor="#ffffff">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <axisSymbol>
        <symbol name="" alpha="1" type="line" clip_to_extent="1" force_rhr="0">
          <layer class="SimpleLine" locked="0" enabled="1" pass="0">
            <prop v="square" k="capstyle"/>
            <prop v="5;2" k="customdash"/>
            <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
            <prop v="MM" k="customdash_unit"/>
            <prop v="0" k="draw_inside_polygon"/>
            <prop v="bevel" k="joinstyle"/>
            <prop v="35,35,35,255" k="line_color"/>
            <prop v="solid" k="line_style"/>
            <prop v="0.26" k="line_width"/>
            <prop v="MM" k="line_width_unit"/>
            <prop v="0" k="offset"/>
            <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
            <prop v="MM" k="offset_unit"/>
            <prop v="0" k="ring_filter"/>
            <prop v="0" k="use_custom_dash"/>
            <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings showAll="1" placement="0" obstacle="0" zIndex="0" dist="0" linePlacementFlags="18" priority="0">
    <properties>
      <Option type="Map">
        <Option name="name" value="" type="QString"/>
        <Option name="properties"/>
        <Option name="type" value="collection" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <referencedLayers/>
  <referencingLayers/>
  <fieldConfiguration>
    <field name="X">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Y">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Z">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="azimuth">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="dip">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="polarity">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="formation">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="X" name="" index="0"/>
    <alias field="Y" name="" index="1"/>
    <alias field="Z" name="" index="2"/>
    <alias field="azimuth" name="" index="3"/>
    <alias field="dip" name="" index="4"/>
    <alias field="polarity" name="" index="5"/>
    <alias field="formation" name="" index="6"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="X" expression="" applyOnUpdate="0"/>
    <default field="Y" expression="" applyOnUpdate="0"/>
    <default field="Z" expression="" applyOnUpdate="0"/>
    <default field="azimuth" expression="" applyOnUpdate="0"/>
    <default field="dip" expression="" applyOnUpdate="0"/>
    <default field="polarity" expression="" applyOnUpdate="0"/>
    <default field="formation" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="X" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="Y" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="Z" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="azimuth" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="dip" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="polarity" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="formation" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="X" exp=""/>
    <constraint desc="" field="Y" exp=""/>
    <constraint desc="" field="Z" exp=""/>
    <constraint desc="" field="azimuth" exp=""/>
    <constraint desc="" field="dip" exp=""/>
    <constraint desc="" field="polarity" exp=""/>
    <constraint desc="" field="formation" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortExpression="" sortOrder="0" actionWidgetStyle="dropDown">
    <columns>
      <column name="X" width="-1" hidden="0" type="field"/>
      <column name="Y" width="-1" hidden="0" type="field"/>
      <column name="Z" width="-1" hidden="0" type="field"/>
      <column name="azimuth" width="-1" hidden="0" type="field"/>
      <column name="dip" width="-1" hidden="0" type="field"/>
      <column name="polarity" width="-1" hidden="0" type="field"/>
      <column name="formation" width="-1" hidden="0" type="field"/>
      <column width="-1" hidden="1" type="actions"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field name="X" editable="1"/>
    <field name="Y" editable="1"/>
    <field name="Z" editable="1"/>
    <field name="azimuth" editable="1"/>
    <field name="dip" editable="1"/>
    <field name="formation" editable="1"/>
    <field name="polarity" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="X" labelOnTop="0"/>
    <field name="Y" labelOnTop="0"/>
    <field name="Z" labelOnTop="0"/>
    <field name="azimuth" labelOnTop="0"/>
    <field name="dip" labelOnTop="0"/>
    <field name="formation" labelOnTop="0"/>
    <field name="polarity" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>X</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
